# -*- coding: utf-8 -*-
"""spider-advanced 内容自检。

用法：
    python check.py            # 检查全站
    python check.py ch09       # 只查某一章

覆盖的六类问题，都是实际踩过的：
  1. 标签配对（div/p/pre/table/span/code...）
  2. 章节编号连续 + h2 与 <!-- ==== x.y ==== --> 注释一致
  3. 打卡项数量 == assets/app.js 里 TOTALS 的值
  4. Markdown 语法残留（裸 ** / 裸 ` 反引号）
  5. 行内代码用了 <code> 而不是站点规范的 <code class="inline">
  6. 未转义的 & 与 <kbd>（站点无此样式）

退出码：0 全部通过；1 有问题。
"""
import re
import sys
import io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).parent

TAG_SETS = ["div", "h2", "h3", "p", "pre", "table", "span", "code",
            "ol", "ul", "li", "thead", "tbody", "tr", "td", "th", "a"]

ALLOWED_ENTITIES = re.compile(r"&(amp|lt|gt|quot|nbsp|mdash|hellip|#\d+|#x[0-9a-fA-F]+);")

# chip 的合法修饰类（style.css 里都有定义；拼错就等于没有样式）
CHIP_CLASSES = {
    "tbook", "tconnect", "tlab", "tanim", "tnew",   # 来源/类型
    "ts-now", "ts-check", "ts-old",                 # 内容时效
}


def load_totals():
    """从 app.js 里解析 TOTALS = { c01: 6, ... }"""
    js = (ROOT / "assets" / "app.js").read_text(encoding="utf-8")
    m = re.search(r"var TOTALS = \{(.*?)\}", js, re.S)
    if not m:
        return {}
    out = {}
    for k, v in re.findall(r"(c\d+)\s*:\s*(\d+)", m.group(1)):
        out[k] = int(v)
    return out


def strip_pre(html):
    """拆两层：
    - no_pre : 只把 <pre> 块换成占位符 —— 用于标签配对、<code> 样式检查
    - no_code: 再把行内 <code>…</code> 的内容也换掉 —— 用于 Markdown 残留、转义检查
      （代码里合法会出现 `**`（JS 幂运算）、裸 `&`（URL 拼接），不能当问题报）
    """
    no_pre = html
    pres = re.findall(r"<pre[^>]*>.*?</pre>", html, re.S)
    for i, _ in enumerate(pres):
        no_pre = no_pre.replace(pres[i], "\x00PRE%d\x00" % i, 1)
    # <script>/<style> 里是 JS/CSS，`&` 和 `**` 都合法，一并排除
    no_pre = re.sub(r"<script[^>]*>.*?</script>", "\x00SCRIPT\x00", no_pre, flags=re.S)
    no_pre = re.sub(r"<style[^>]*>.*?</style>", "\x00STYLE\x00", no_pre, flags=re.S)
    no_code = re.sub(r"<code([^>]*)>.*?</code>", r"<code\1></code>", no_pre, flags=re.S)
    return no_pre, no_code


def check_file(path, totals, chapter_key):
    problems = []
    html = path.read_text(encoding="utf-8")
    name = path.name

    # ---------- 1. 标签配对 ----------
    for t in TAG_SETS:
        o = len(re.findall(r"<%s[\s>]" % t, html))
        c = html.count("</%s>" % t)
        if o != c:
            problems.append("[标签] <%s> 开 %d / 闭 %d，不配对" % (t, o, c))

    body, txt = strip_pre(html)

    # ---------- 2. 编号连续性 + 注释一致 ----------
    # 一级小节是 <h2>，二级编号小节可能是 <h3>（如 ch10 的 10.11），两者一起看
    h2_nums = re.findall(r"<h2>(\d+)\.(\d+)\s", body)
    if h2_nums:
        ch = h2_nums[0][0]
        secs = [int(b) for a, b in h2_nums if a == ch]
        expect = list(range(1, len(secs) + 1))
        if secs != expect:
            problems.append("[编号] h2 序号不连续：%s （应为 1..%d）" % (secs, len(secs)))
        # 注释与「h2 + 带编号的 h3」对齐
        all_secs = [int(b) for a, b in
                    re.findall(r"<h[23]>(\d+)\.(\d+)\s", body) if a == ch]
        all_secs = sorted(set(all_secs))
        cmts = [int(b) for a, b in
                re.findall(r"<!--\s*=+\s*(\d+)\.(\d+)\s*=+\s*-->", body) if a == ch]
        if cmts:
            # 允许首节没写注释（原站风格），但每个注释必须对应真实小节，且递增
            orphan = [c for c in cmts if c not in all_secs]
            if orphan:
                problems.append("[编号] 注释 %s 找不到对应的小节（顺延编号时漏改注释会导致插错位置）"
                                % ["%s.%d" % (ch, o) for o in orphan])
            elif cmts != sorted(cmts):
                problems.append("[编号] 注释顺序乱：%s" % cmts)

    # ---------- 3. 打卡项数量 ----------
    boxes = len(re.findall(r'type="checkbox"\s+id="c\d+-\d+"', body))
    if chapter_key and chapter_key in totals:
        if boxes != totals[chapter_key]:
            problems.append("[打卡] 实际 %d 个 checkbox，但 app.js TOTALS 里 %s = %d"
                            % (boxes, chapter_key, totals[chapter_key]))
    elif boxes:
        problems.append("[打卡] 有 %d 个 checkbox，但 app.js TOTALS 里没有对应的 %s"
                        % (boxes, chapter_key))

    # ---------- 4. Markdown 残留（只看正文，不含行内代码） ----------
    for m in re.finditer(r"\*\*", txt):
        s = txt[max(0, m.start() - 30):m.start() + 30].replace("\n", " ")
        problems.append("[残留] 裸 ** 加粗语法：...%s..." % s)
        break
    for m in re.finditer(r"`", txt):
        s = txt[max(0, m.start() - 30):m.start() + 30].replace("\n", " ")
        problems.append("[残留] 裸 ` 反引号（应改成 <code class=\"inline\">）：...%s..." % s)
        break

    # ---------- 5. <code> 样式规范 ----------
    bare = len(re.findall(r"<code>", body))
    if bare:
        problems.append('[样式] %d 处 <code> 缺少 class="inline"，站内有 1178 处用的是 inline 版' % bare)

    # ---------- 6. 转义（只看正文，不含行内代码） ----------
    bad_amp = []
    for m in re.finditer(r"&", txt):
        if not ALLOWED_ENTITIES.match(txt, m.start()):
            bad_amp.append(txt[max(0, m.start() - 25):m.start() + 25].replace("\n", " "))
    if bad_amp:
        problems.append("[转义] %d 处未转义的 &：...%s..." % (len(bad_amp), bad_amp[0]))
    for m in re.finditer(r"<kbd>", txt):
        problems.append("[样式] 用了 <kbd>，站点 CSS 未定义该样式，改用 <code class=\"inline\">")
        break

    # ---------- 7. chip 类名白名单（防手滑拼错，错了就是没样式） ----------
    unknown = set()
    for m in re.finditer(r'class="chip((?:\s+[a-z0-9-]+)*)"', body):
        for c in m.group(1).split():
            if c not in CHIP_CLASSES:
                unknown.add(c)
    if unknown:
        problems.append("[样式] 未知 chip 修饰类：%s（白名单见 check.py 顶部 CHIP_CLASSES）"
                        % ", ".join(sorted(unknown)))

    # ---------- 8. 每章必须有「内容基准」块 ----------
    if chapter_key and 'class="basis-note"' not in html:
        problems.append('[时效] 缺少「内容基准」块（<div class="basis-note">），'
                        '读者无法判断本章素材的年代')

    return problems


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else None
    totals = load_totals()

    pages = sorted(ROOT.glob("ch*.html"))
    if target:
        pages = [p for p in pages if p.stem == target]

    total_problems = 0
    for p in pages:
        m = re.match(r"ch(\d+)", p.stem)
        key = ("c%02d" % int(m.group(1))) if m else None
        probs = check_file(p, totals, key)
        if probs:
            total_problems += len(probs)
            print("\n%s  (%d 个问题)" % (p.name, len(probs)))
            for x in probs:
                print("   -", x)
        else:
            print("%-12s OK" % p.name)

    # index.html 也过一遍标签与残留检查（没有章节编号，跳过打卡/编号）
    if not target:
        probs = check_file(ROOT / "index.html", {}, None)
        probs = [x for x in probs if not x.startswith("[标签]")] + \
                [x for x in probs if x.startswith("[标签]")]
        real = [x for x in probs if not x.startswith("[打卡]")]
        if real:
            total_problems += len(real)
            print("\nindex.html  (%d 个问题)" % len(real))
            for x in real:
                print("   -", x)
        else:
            print("%-12s OK" % "index.html")

    print("\n" + ("全部通过。" if total_problems == 0 else "共 %d 个问题。" % total_problems))
    return 0 if total_problems == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

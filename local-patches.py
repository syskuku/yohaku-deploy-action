#!/usr/bin/env python3
"""Local patches applied at build time on top of upstream innei-dev/Yohaku.
Owner-approved customizations; every hunk prints APPLIED or SKIPPED.
SKIPPED means upstream changed the code — revisit this script."""
import io, os, sys

PATCHES = []

def patch(path, old, new, name, required=False):
    PATCHES.append((path, old, new, name, required))

# --- 1. footer reading-rooms lookup: article_ -> article- (upstream bug) ---
patch('apps/web/src/components/layout/footer/GatewayInfo.tsx',
      'const roomName = (id: string) => `article_${id}`',
      'const roomName = (id: string) => `article-${id}`',
      'GatewayInfo roomName hyphen')

# --- 2. OG cards: LXGW WenKai -> MiSans (TTFs installed at /usr/local/share/fonts/misans) ---
patch('apps/web/src/lib/og-shared.ts',
      "const lxgwRegularFonts = [\n  'LXGWWenKai-Regular.ttf',\n  'LXGWWenKaiMono-Regular.ttf',\n  'Arial Unicode 2.ttf',\n]",
      "const lxgwRegularFonts = [\n  'misans/MiSans-Regular.ttf',\n  'MiSans-Regular.ttf',\n]",
      'og regular fonts -> MiSans')
patch('apps/web/src/lib/og-shared.ts',
      "const lxgwMediumFonts = [\n  'LXGWWenKai-Medium.ttf',\n  'LXGWWenKaiMono-Medium.ttf',\n  'Arial Unicode 2.ttf',\n]",
      "const lxgwMediumFonts = [\n  'misans/MiSans-Medium.ttf',\n  'MiSans-Medium.ttf',\n]",
      'og medium fonts -> MiSans')
patch('apps/web/src/lib/og-shared.ts',
      ': \'\"LXGW WenKai\", system-ui, sans-serif\'',
      ': \'"MiSans", system-ui, sans-serif\'',
      'og fontFamily -> MiSans')
patch('apps/web/src/lib/og-shared.ts',
      "const name = useGeist ? 'Geist' : 'LXGW WenKai'",
      "const name = useGeist ? 'Geist' : 'MiSans'",
      'og font name -> MiSans')

# --- 3. note-font loader: lxgw css -> misans.css ---
patch('yohaku-oss/packages/rich-content/src/lexical/portable/excalidraw/use-lxgw-font.ts',
      "const LXGW_HREF = '/fonts/excalidraw/lxgw/lxgw-wenkai-screen.css'",
      "const LXGW_HREF = '/fonts/misans.css'",
      'excalidraw font loader -> misans.css')

# --- 4. excalidraw hand-font stack: LXGW -> MiSans ---
patch('yohaku-oss/packages/rich-content/src/lexical/portable/excalidraw/fonts.ts',
      '"Excalifont", "LXGW WenKai Screen", "Virgil"',
      '"Excalifont", "MiSans", "Virgil"',
      'excalidraw hand stack -> MiSans')

# --- 5. excalidraw fullscreen @import -> misans.css ---
patch('yohaku-oss/packages/rich-content/src/lexical/portable/excalidraw/open-in-new-window.ts',
      "@import url('${origin}/fonts/excalidraw/lxgw/lxgw-wenkai-screen.css');",
      "@import url('${origin}/fonts/misans.css');",
      'excalidraw fullscreen @import -> misans')

# --- 6. note font switcher label + family ---
patch('apps/web/src/components/modules/note/NoteFontFab.tsx',
      "  lxgw: {\n    name: '霞鹜文楷',\n    family: `'LXGW WenKai Screen', var(--font-sans), var(--font-serif), system-ui`,\n  },",
      "  lxgw: {\n    name: 'MiSans',\n    family: `'MiSans', var(--font-sans), var(--font-serif), system-ui`,\n  },",
      'note font switcher -> MiSans')

# --- 7. footer motto (all locales) ---
for loc in ('zh', 'zh-TW', 'ja', 'ko', 'en'):
    patch(f'apps/web/src/messages/{loc}/common.json',
          '"footer_motto": "Stay hungry. Stay foolish.",',
          '"footer_motto": "Developer by skill, otaku by heart.",',
          f'footer_motto ({loc})')


# --- 8. kodo 图片瘦身（SSR HTML 天生带参，绕过 preload scanner 抢跑原图）---
# markdown 图片渲染器（note + posts 共用 MarkdownImage）
patch('apps/web/src/components/ui/markdown/renderers/image.tsx',
      "  const { src, alt } = props\n"
      "  const nextProps = {\n"
      "    ...props,\n"
      "    alt: alt?.replace(/^[!¡]/, ''),\n"
      "  }",
      "const KODO_PARAMS: Record<string, string> = {\n"
      "  3hfhhfvatzozqlkcsu.png: 'resize/3072x3072%3E/quality/85/format/webp',\n"
      "  3znx81kvi0e7zmz41c.jpg: 'resize/3072x3072%3E/quality/84/format/jpg',\n"
      "  74kisoynfte3sip71p.jpg: 'resize/3072x3072%3E/quality/84/format/jpg',\n"
      "  7rg1oxx4ysqmjt841g.jpg: 'resize/3072x3072%3E/quality/80/format/jpg',\n"
      "  axa81mm9xltknl1muy.jpg: 'resize/3072x3072%3E/quality/76/format/jpg',\n"
      "  c3x9oaa5z9lbf2sz72.jpg: 'resize/3072x3072%3E/quality/80/format/jpg',\n"
      "  cxikvatj3a3g6zlaw2.jpg: 'resize/3072x3072%3E/quality/88/format/jpg',\n"
      "  hej6zcd2n9upvqrvya.jpg: 'resize/3072x3072%3E/quality/84/format/jpg',\n"
      "  ispvdzow974u3cfylc.jpg: 'resize/3072x3072%3E/quality/84/format/jpg',\n"
      "  m2flcht92qlh7ksch2.jpg: 'resize/3072x3072%3E/quality/88/format/jpg',\n"
      "  mdy7eenvbfr1tyeoq7.jpg: 'resize/3072x3072%3E/quality/82/format/jpg',\n"
      "  ndfxu0i9kubfz0zydx.jpg: 'resize/3072x3072%3E/quality/86/format/jpg',\n"
      "  oguv8t4c9bc82wppzy.jpg: 'resize/2560x2560%3E/quality/82/format/jpg',\n"
      "  p5jq1o4xrk9k4ys7tk.png: 'resize/2048x2048%3E/quality/89/format/webp',\n"
      "  umcri083sb9jsj2xhc.jpg: 'resize/3072x3072%3E/quality/82/format/jpg',\n"
      "}\n"
      "const KODO_DEFAULT = 'resize/3072x3072%3E/quality/82/format/jpg'\n"
      "function kodoSlim(src: string): string {\n"
      "  if (!src || !src.includes('kodo.imikufans.com') || src.includes('imageMogr2')) return src\n"
      "  if (!/\\.(png|jpe?g|webp|gif|avif)(\\?|$)/i.test(src)) return src\n"
      "  const name = src.split('?')[0].split('/').pop() || ''\n"
      "  return src + '?imageMogr2/' + (KODO_PARAMS[name] || KODO_DEFAULT)\n"
      "}\n"
      "\n"
      "  const { alt } = props\n"
      "  const src = kodoSlim(props.src)\n"
      "  const nextProps = {\n"
      "    ...props,\n"
      "    src,\n"
      "    alt: alt?.replace(/^[!¡]/, ''),\n"
      "  }",
      'kodo slim: MarkdownImage src')

# lexical 笔记图片节点（yohaku-oss）
patch('yohaku-oss/packages/rich-content/src/lexical/portable/image.tsx',
      "export function LexicalImageOverride(props: ImageRendererProps) {\n  const [frame, setFrame] = useState<HTMLElement | null>(null)",
      "export function LexicalImageOverride(props: ImageRendererProps) {\n"
      "const KODO_PARAMS: Record<string, string> = {\n"
      "  3hfhhfvatzozqlkcsu.png: 'resize/3072x3072%3E/quality/85/format/webp',\n"
      "  3znx81kvi0e7zmz41c.jpg: 'resize/3072x3072%3E/quality/84/format/jpg',\n"
      "  74kisoynfte3sip71p.jpg: 'resize/3072x3072%3E/quality/84/format/jpg',\n"
      "  7rg1oxx4ysqmjt841g.jpg: 'resize/3072x3072%3E/quality/80/format/jpg',\n"
      "  axa81mm9xltknl1muy.jpg: 'resize/3072x3072%3E/quality/76/format/jpg',\n"
      "  c3x9oaa5z9lbf2sz72.jpg: 'resize/3072x3072%3E/quality/80/format/jpg',\n"
      "  cxikvatj3a3g6zlaw2.jpg: 'resize/3072x3072%3E/quality/88/format/jpg',\n"
      "  hej6zcd2n9upvqrvya.jpg: 'resize/3072x3072%3E/quality/84/format/jpg',\n"
      "  ispvdzow974u3cfylc.jpg: 'resize/3072x3072%3E/quality/84/format/jpg',\n"
      "  m2flcht92qlh7ksch2.jpg: 'resize/3072x3072%3E/quality/88/format/jpg',\n"
      "  mdy7eenvbfr1tyeoq7.jpg: 'resize/3072x3072%3E/quality/82/format/jpg',\n"
      "  ndfxu0i9kubfz0zydx.jpg: 'resize/3072x3072%3E/quality/86/format/jpg',\n"
      "  oguv8t4c9bc82wppzy.jpg: 'resize/2560x2560%3E/quality/82/format/jpg',\n"
      "  p5jq1o4xrk9k4ys7tk.png: 'resize/2048x2048%3E/quality/89/format/webp',\n"
      "  umcri083sb9jsj2xhc.jpg: 'resize/3072x3072%3E/quality/82/format/jpg',\n"
      "}\n"
      "const KODO_DEFAULT = 'resize/3072x3072%3E/quality/82/format/jpg'\n"
      "function kodoSlim(src: string): string {\n"
      "  if (!src || !src.includes('kodo.imikufans.com') || src.includes('imageMogr2')) return src\n"
      "  if (!/\\.(png|jpe?g|webp|gif|avif)(\\?|$)/i.test(src)) return src\n"
      "  const name = src.split('?')[0].split('/').pop() || ''\n"
      "  return src + '?imageMogr2/' + (KODO_PARAMS[name] || KODO_DEFAULT)\n"
      "}\n"
      "\n"
      "  const src = kodoSlim(props.src)\n"
      "  const [frame, setFrame] = useState<HTMLElement | null>(null)",
      'kodo slim: lexical src')
patch('yohaku-oss/packages/rich-content/src/lexical/portable/image.tsx',
      '<ComposedImageRenderer {...props} />',
      '<ComposedImageRenderer {...props} src={src} />',
      'kodo slim: lexical renderer src')
patch('yohaku-oss/packages/rich-content/src/lexical/portable/image.tsx',
      '<ImageExifOverlay src={props.src} />',
      '<ImageExifOverlay src={src} />',
      'kodo slim: lexical exif src')

def main():
    failed = []
    for path, old, new, name, required in PATCHES:
        full = path
        if not os.path.exists(full):
            print(f'SKIPPED [{name}] file missing: {path}')
            if required:
                failed.append(name)
            continue
        s = io.open(full, encoding='utf-8').read()
        if old not in s:
            print(f'SKIPPED [{name}] pattern not found (upstream changed?)')
            if required:
                failed.append(name)
            continue
        if s.count(old) > 1:
            print(f'SKIPPED [{name}] pattern ambiguous ({s.count(old)} hits)')
            if required:
                failed.append(name)
            continue
        io.open(full, 'w', encoding='utf-8').write(s.replace(old, new, 1))
        print(f'APPLIED [{name}]')
    if failed:
        print('FATAL required patches failed:', failed)
        sys.exit(1)
    print(f'done: {len(PATCHES)} hunks attempted')

if __name__ == '__main__':
    main()

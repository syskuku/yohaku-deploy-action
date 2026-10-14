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
      "  const { alt } = props\n"
      "  const src = /\\.(png|jpe?g|webp|gif|avif)(\\?|$)/i.test(props.src) &&\n"
      "    props.src.includes('kodo.imikufans.com') &&\n"
      "    !props.src.includes('imageMogr2')\n"
      "    ? props.src + '?imageMogr2/resize/2048x2048%3E/quality/90/format/webp'\n"
      "    : props.src\n"
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
      "  const src = /\\.(png|jpe?g|webp|gif|avif)(\\?|$)/i.test(props.src || '') &&\n"
      "    (props.src || '').includes('kodo.imikufans.com') &&\n"
      "    !(props.src || '').includes('imageMogr2')\n"
      "    ? props.src + '?imageMogr2/resize/2048x2048%3E/quality/90/format/webp'\n"
      "    : props.src\n"
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

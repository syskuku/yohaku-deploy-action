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
      "  '3hfhhfvatzozqlkcsu.png': 'resize/3072x3072%3E/quality/85/format/webp',\n"
      "  '3znx81kvi0e7zmz41c.jpg': 'resize/3072x3072%3E/quality/84/format/jpg',\n"
      "  '74kisoynfte3sip71p.jpg': 'resize/3072x3072%3E/quality/84/format/jpg',\n"
      "  '7rg1oxx4ysqmjt841g.jpg': 'resize/3072x3072%3E/quality/80/format/jpg',\n"
      "  'axa81mm9xltknl1muy.jpg': 'resize/3072x3072%3E/quality/76/format/jpg',\n"
      "  'c3x9oaa5z9lbf2sz72.jpg': 'resize/3072x3072%3E/quality/80/format/jpg',\n"
      "  'cxikvatj3a3g6zlaw2.jpg': 'resize/3072x3072%3E/quality/88/format/jpg',\n"
      "  'hej6zcd2n9upvqrvya.jpg': 'resize/3072x3072%3E/quality/84/format/jpg',\n"
      "  'ispvdzow974u3cfylc.jpg': 'resize/3072x3072%3E/quality/84/format/jpg',\n"
      "  'm2flcht92qlh7ksch2.jpg': 'resize/3072x3072%3E/quality/88/format/jpg',\n"
      "  'mdy7eenvbfr1tyeoq7.jpg': 'resize/3072x3072%3E/quality/82/format/jpg',\n"
      "  'ndfxu0i9kubfz0zydx.jpg': 'resize/3072x3072%3E/quality/86/format/jpg',\n"
      "  'oguv8t4c9bc82wppzy.jpg': 'resize/2560x2560%3E/quality/82/format/jpg',\n"
      "  'p5jq1o4xrk9k4ys7tk.png': 'resize/2048x2048%3E/quality/89/format/webp',\n"
      "  'umcri083sb9jsj2xhc.jpg': 'resize/3072x3072%3E/quality/82/format/jpg',\n"
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
      "  '3hfhhfvatzozqlkcsu.png': 'resize/3072x3072%3E/quality/85/format/webp',\n"
      "  '3znx81kvi0e7zmz41c.jpg': 'resize/3072x3072%3E/quality/84/format/jpg',\n"
      "  '74kisoynfte3sip71p.jpg': 'resize/3072x3072%3E/quality/84/format/jpg',\n"
      "  '7rg1oxx4ysqmjt841g.jpg': 'resize/3072x3072%3E/quality/80/format/jpg',\n"
      "  'axa81mm9xltknl1muy.jpg': 'resize/3072x3072%3E/quality/76/format/jpg',\n"
      "  'c3x9oaa5z9lbf2sz72.jpg': 'resize/3072x3072%3E/quality/80/format/jpg',\n"
      "  'cxikvatj3a3g6zlaw2.jpg': 'resize/3072x3072%3E/quality/88/format/jpg',\n"
      "  'hej6zcd2n9upvqrvya.jpg': 'resize/3072x3072%3E/quality/84/format/jpg',\n"
      "  'ispvdzow974u3cfylc.jpg': 'resize/3072x3072%3E/quality/84/format/jpg',\n"
      "  'm2flcht92qlh7ksch2.jpg': 'resize/3072x3072%3E/quality/88/format/jpg',\n"
      "  'mdy7eenvbfr1tyeoq7.jpg': 'resize/3072x3072%3E/quality/82/format/jpg',\n"
      "  'ndfxu0i9kubfz0zydx.jpg': 'resize/3072x3072%3E/quality/86/format/jpg',\n"
      "  'oguv8t4c9bc82wppzy.jpg': 'resize/2560x2560%3E/quality/82/format/jpg',\n"
      "  'p5jq1o4xrk9k4ys7tk.png': 'resize/2048x2048%3E/quality/89/format/webp',\n"
      "  'umcri083sb9jsj2xhc.jpg': 'resize/3072x3072%3E/quality/82/format/jpg',\n"
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


# --- 9. 首页社交图标：主页 + 画廊类型 ---
patch('apps/web/src/components/modules/home/SocialIcon.tsx',
      "  mail: [\n    'Email',\n    <i className=\"i-mingcute-mail-line\" />,",
      "  home: ['主页', <i className=\"i-mingcute-home-1-line\" />, '#171717', (id) => id],\n"
      "  gallery: [\n"
      "    '画廊',\n"
      "    <i className=\"i-mingcute-photo-album-line\" />,\n"
      "    '#F5A623',\n"
      "    (id) => id,\n"
      "  ],\n"
      "  mail: [\n    'Email',\n    <i className=\"i-mingcute-mail-line\" />,",
      'social icons: home + gallery')


# --- 10. GitHub/link 卡片渲染（PortableLinkCard + 客户端 enrichment）---
patch('apps/web/src/components/ui/rich-content/LexicalContent.tsx',
      "import { useEffect, useMemo } from 'react'",
      "import { useEffect, useMemo, useState } from 'react'",
      'link-card: useState import')

patch('apps/web/src/components/ui/rich-content/LexicalContent.tsx',
      "import { BlockLinkRenderer } from '~/components/ui/markdown/renderers/LinkRenderer'\n",
      "",
      'link-card: drop unused import')

patch('apps/web/src/components/ui/rich-content/LexicalContent.tsx',
      "  BlockLinkCard: ({ fallback, url }) => (\n"
      "    <BlockLinkRenderer fallback={fallback} href={url} />\n"
      "  ),\n",
      "  // BlockLinkCard: 不覆盖，交给 PortableLinkCard 渲染真卡片\n",
      'link-card: drop plain-link slot')

patch('apps/web/src/components/ui/rich-content/LexicalContent.tsx',
      "const richContentSlots: HostCapabilities['slots'] = {",
      "type LinkCardEnrichment = {\n"
      "  attributes?: Array<{\n"
      "    format?: string\n"
      "    key: string\n"
      "    label?: string\n"
      "    value: boolean | number | string\n"
      "  }>\n"
      "  category?: string\n"
      "  color?: string\n"
      "  description?: string\n"
      "  subtype?: string\n"
      "  title: string\n"
      "  url: string\n"
      "}\n"
      "\n"
      "const linkCardCache = new Map<string, LinkCardEnrichment | null>()\n"
      "\n"
      "function collectLinkCardUrls(node: unknown, out: Set<string>) {\n"
      "  if (!node || typeof node !== 'object') return\n"
      "  const n = node as Record<string, any>\n"
      "  if (n.type === 'link-card' && typeof n.url === 'string') out.add(n.url)\n"
      "  for (const v of Object.values(n)) {\n"
      "    if (v && typeof v === 'object') collectLinkCardUrls(v, out)\n"
      "  }\n"
      "}\n"
      "\n"
      "const GITHUB_RESERVED = new Set([\n"
      "  'about', 'apps', 'collections', 'events', 'explore', 'features', 'issues',\n"
      "  'login', 'marketplace', 'new', 'notifications', 'orgs', 'pricing', 'pulls',\n"
      "  'search', 'settings', 'signup', 'sponsors', 'topics', 'trending',\n"
      "])\n"
      "\n"
      "async function resolveLinkCard(url: string): Promise<LinkCardEnrichment | null> {\n"
      "  try {\n"
      "    const gh = /^https?:\\/\\/github\\.com\\/([^/?#]+)\\/([^/?#]+)\\/?(?:[?#].*)?$/i.exec(url)\n"
      "    if (gh && !GITHUB_RESERVED.has(gh[1].toLowerCase())) {\n"
      "      const res = await fetch(`https://api.github.com/repos/${gh[1]}/${gh[2]}`, {\n"
      "        headers: { Accept: 'application/vnd.github+json' },\n"
      "      })\n"
      "      if (!res.ok) return null\n"
      "      const d = await res.json()\n"
      "      return {\n"
      "        attributes: [\n"
      "          { format: 'number', key: 'stars', label: 'Stars', value: Number(d.stargazers_count) || 0 },\n"
      "          { format: 'number', key: 'forks', label: 'Forks', value: Number(d.forks_count) || 0 },\n"
      "          ...(d.language ? [{ key: 'language', label: 'Language', value: String(d.language) }] : []),\n"
      "        ],\n"
      "        category: 'github',\n"
      "        color: '#181717',\n"
      "        description: typeof d.description === 'string' ? d.description : '',\n"
      "        subtype: d.fork ? 'fork' : 'repo',\n"
      "        title: String(d.full_name || `${gh[1]}/${gh[2]}`),\n"
      "        url,\n"
      "      }\n"
      "    }\n"
      "    const res = await fetch(`/api/v3/enrichment/resolve?url=${encodeURIComponent(url)}`)\n"
      "    if (res.status !== 200) return null\n"
      "    const json = await res.json()\n"
      "    const data = json?.data\n"
      "    return data && typeof data.title === 'string' ? { ...data, url } : null\n"
      "  } catch {\n"
      "    return null\n"
      "  }\n"
      "}\n"
      "\n"
      "function useLinkCardEnrichments(content: unknown): Record<string, LinkCardEnrichment> {\n"
      "  const [map, setMap] = useState<Record<string, LinkCardEnrichment>>({})\n"
      "  useEffect(() => {\n"
      "    const urls = new Set<string>()\n"
      "    collectLinkCardUrls(content, urls)\n"
      "    const cachedMap: Record<string, LinkCardEnrichment> = {}\n"
      "    const missing: string[] = []\n"
      "    for (const u of urls) {\n"
      "      if (linkCardCache.has(u)) {\n"
      "        const v = linkCardCache.get(u)\n"
      "        if (v) cachedMap[u] = v\n"
      "      } else {\n"
      "        missing.push(u)\n"
      "      }\n"
      "    }\n"
      "    if (Object.keys(cachedMap).length) {\n"
      "      setMap((prev) => ({ ...prev, ...cachedMap }))\n"
      "    }\n"
      "    if (!missing.length) return\n"
      "    let cancelled = false\n"
      "    void Promise.all(\n"
      "      missing.slice(0, 12).map(async (u) => [u, await resolveLinkCard(u)] as const),\n"
      "    ).then((pairs) => {\n"
      "      if (cancelled) return\n"
      "      const next: Record<string, LinkCardEnrichment> = {}\n"
      "      for (const [u, v] of pairs) {\n"
      "        linkCardCache.set(u, v)\n"
      "        if (v) next[u] = v\n"
      "      }\n"
      "      if (Object.keys(next).length) setMap((prev) => ({ ...prev, ...next }))\n"
      "    })\n"
      "    return () => {\n"
      "      cancelled = true\n"
      "    }\n"
      "  }, [content])\n"
      "  return map\n"
      "}\n"
      "const richContentSlots: HostCapabilities['slots'] = {"
      '',
      'link-card: enrichment helper')

patch('apps/web/src/components/ui/rich-content/LexicalContent.tsx',
      "  const webHost = useWebHost({\n"
      "    nestedDocPresentation: 'modal',\n"
      "    slots: richContentSlots,\n"
      "  })\n",
      "  const webHost = useWebHost({\n"
      "    nestedDocPresentation: 'modal',\n"
      "    slots: richContentSlots,\n"
      "  })\n"
      "  const linkCardEnrichments = useLinkCardEnrichments(content)\n"
      "  const hostedWebHost = useMemo(\n"
      "    () =>\n"
      "      Object.keys(linkCardEnrichments).length\n"
      "        ? { ...webHost, enrichments: linkCardEnrichments }\n"
      "        : webHost,\n"
      "    [webHost, linkCardEnrichments],\n"
      "  )\n",
      'link-card: hosted web host')

patch('apps/web/src/components/ui/rich-content/LexicalContent.tsx',
      "    <HostProvider host={webHost}>\n"
      "      <RichContentBody",
      "    <HostProvider host={hostedWebHost}>\n"
      "      <RichContentBody",
      'link-card: main host provider')

patch('apps/web/src/components/ui/rich-content/LexicalContent.tsx',
      "        <HostProvider host={webHost}>{nestedContent}</HostProvider>",
      "        <HostProvider host={hostedWebHost}>{nestedContent}</HostProvider>",
      'link-card: nested host provider')

patch('apps/web/src/components/ui/rich-content/LexicalContent.tsx',
      "  }, [isMobile, present, webHost])",
      "  }, [isMobile, present, hostedWebHost])",
      'link-card: effect deps')

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

# 14. Frontend, for full-stack roles (P2 — only if the job says full stack)

Many 3-year roles in Bengaluru are titled "full stack". Your LinkedIn lists React, Next.js and React Native, and
you wrote an article on React Server Components, so expect a few questions even in backend-leaning rounds.

---

## 14.1 Browser basics
- [ ] How a page renders: HTML → DOM, CSS → CSSOM, render tree, layout, paint, composite ↳ Google "Inside look at modern web browser" parts 1–4 (developer.chrome.com/blog) · MDN "Critical rendering path" (developer.mozilla.org) · https://github.com/alex/what-happens-when
- [ ] Reflow vs repaint; what triggers layout thrashing ↳ web.dev "Avoid large, complex layouts and layout thrashing" (web.dev) · Paul Irish "What forces layout / reflow" (gist.github.com/paulirish)
- [ ] Event bubbling/capturing, delegation; `preventDefault` vs `stopPropagation` ↳ https://javascript.info/bubbling-and-capturing · https://javascript.info/event-delegation · https://javascript.info/default-browser-action
- [ ] Storage: cookies vs localStorage vs sessionStorage vs IndexedDB ↳ https://javascript.info/cookie · https://javascript.info/localstorage · https://javascript.info/indexeddb
- [ ] Same-origin policy, CORS from the browser side; CSP ↳ https://javascript.info/fetch-crossorigin · MDN "Same-origin policy" + "Content Security Policy (CSP)" (developer.mozilla.org)

**Questions:** What happens between the HTML arriving and the first paint? · Event delegation — why?

## 14.2 React
- [ ] Rendering and reconciliation; keys and why index keys break lists ↳ https://react.dev/learn/rendering-lists ("Keeping list items in order with key") · https://react.dev/learn/preserving-and-resetting-state · https://react.dev/learn/render-and-commit
- [ ] Hooks: `useState`, `useEffect` (dependency pitfalls, cleanup), `useRef`, `useMemo`, `useCallback`, custom hooks ↳ https://react.dev/learn/synchronizing-with-effects · https://react.dev/learn/you-might-not-need-an-effect · https://react.dev/learn/reusing-logic-with-custom-hooks
- [ ] When components re-render; `React.memo`; lifting state; context and its re-render cost ↳ https://react.dev/reference/react/memo · https://overreacted.io/before-you-memo/ · https://react.dev/learn/passing-data-deeply-with-context
- [ ] State management: local vs server state (TanStack Query) vs global (Redux Toolkit, Zustand) ↳ https://react.dev/learn/managing-state · TanStack Query docs "Overview" (tanstack.com/query) · TkDodo "Practical React Query" blog series (tkdodo.eu)
- [ ] Forms and controlled vs uncontrolled inputs ↳ https://react.dev/reference/react-dom/components/input ("Controlling an input with a state variable") · https://react.dev/learn/sharing-state-between-components ("Controlled and uncontrolled components")
- [ ] Error boundaries, Suspense, lazy loading ↳ https://react.dev/reference/react/Component (catching rendering errors with an error boundary) · https://react.dev/reference/react/Suspense · https://react.dev/reference/react/lazy

**Questions:** Why does my `useEffect` run twice? · `useMemo` vs `useCallback`? · How would you stream LLM tokens
into a chat UI without re-rendering the whole list?

## 14.3 Next.js and rendering strategies
- [ ] CSR vs SSR vs SSG vs ISR; hydration and its cost ↳ https://web.dev/articles/rendering-on-the-web · nextjs.org/docs "Rendering" pages (SSR, SSG, ISR) · patterns.dev "Rendering patterns"
- [ ] App Router, Server Components vs Client Components, server actions ↳ https://react.dev/reference/rsc/server-components · nextjs.org/docs/app "Server and Client Components" + "Server Actions and Mutations" (nextjs.org/docs)
- [ ] Data fetching and caching in Next.js; streaming with Suspense ↳ nextjs.org/docs/app "Caching in Next.js" + "Loading UI and Streaming" (nextjs.org/docs) · https://react.dev/reference/react/Suspense
- [ ] SEO basics (you lifted SEO 30% at Jigsaw): meta tags, sitemaps, Core Web Vitals ↳ https://developers.google.com/search/docs/fundamentals/seo-starter-guide · nextjs.org/docs/app "Metadata" + "sitemap.xml" (nextjs.org/docs) · https://web.dev/articles/vitals

**Questions:** When would you choose SSR over SSG? · Why do RSCs send data twice? (your own article)

## 14.4 Performance and accessibility
- [ ] Core Web Vitals: LCP, INP, CLS — what moves each ↳ https://web.dev/articles/vitals · https://web.dev/articles/lcp · https://web.dev/articles/inp (and web.dev/articles/cls)
- [ ] Code splitting, image optimisation, caching static assets, CDN ↳ https://react.dev/reference/react/lazy · https://web.dev/articles/http-cache · https://www.cloudflare.com/learning/cdn/what-is-a-cdn/
- [ ] Accessibility: semantic HTML, labels, keyboard navigation, focus, contrast ↳ https://web.dev/learn/accessibility · https://www.w3.org/WAI/ARIA/apg/ · https://webaim.org/resources/contrastchecker/

## 14.5 React Native (only if the role mentions mobile)
- [ ] Architecture (JS thread, native modules, new architecture idea), navigation, offline storage, push notifications ↳ reactnative.dev "Architecture overview" (New Architecture) · https://reactnavigation.org/docs/getting-started · Expo docs "Push notifications overview" (docs.expo.dev)

**Learn:** react.dev (Learn section: "Thinking in React", "Escape hatches", "You might not need an effect") ·
nextjs.org/docs (App Router, rendering, caching) · web.dev (Core Web Vitals, rendering performance) ·
developer.mozilla.org (DOM events, storage) · greatfrontend.com (free questions)

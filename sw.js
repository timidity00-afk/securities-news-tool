// 항상 네트워크 우선(최신 데이터), 연결이 없을 때만 마지막으로 본 화면을 보여줌
const C = "securities-v1";
self.addEventListener("install", () => self.skipWaiting());
self.addEventListener("activate", e => e.waitUntil(
  caches.keys().then(ks => Promise.all(ks.filter(k => k !== C).map(k => caches.delete(k)))).then(() => self.clients.claim())));
self.addEventListener("fetch", e => {
  const u = new URL(e.request.url);
  if (e.request.method !== "GET" || u.origin !== location.origin) return;
  e.respondWith(fetch(e.request).then(r => {
    if (r.ok) { const c = r.clone(); caches.open(C).then(x => x.put(u.origin + u.pathname, c)); }
    return r;
  }).catch(() => caches.match(u.origin + u.pathname)));
});

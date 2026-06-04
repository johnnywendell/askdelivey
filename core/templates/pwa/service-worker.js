const CACHE_NAME = 'askdelivery-v3';

self.addEventListener('install', event => {

    self.skipWaiting();
});

self.addEventListener('activate', event => {

    self.clients.claim();
});

self.addEventListener('fetch', event => {

    if (
        event.request.method !== 'GET' ||

        event.request.url.includes('/admin/') ||
        event.request.url.includes('/api/') ||
        event.request.url.includes('/login/') ||
        event.request.url.includes('/logout/')
    ) {
        return;
    }

    event.respondWith(

        fetch(event.request)
            .catch(() => caches.match(event.request))
    );
});
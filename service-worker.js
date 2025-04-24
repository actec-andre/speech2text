const CACHE_NAME = 'sprach-diktierer-v1';
const ASSETS_TO_CACHE = [
  '/',
  '/index.html',
  '/manifest.json',
  '/favicon.png',
  'https://cdn.jsdelivr.net/npm/@stlite/browser@0.76.0/build/style.css',
  'https://cdn.jsdelivr.net/npm/@stlite/browser@0.76.0/build/stlite.js'
];

// Service Worker Installation - Cache Dateien
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Cache geöffnet');
        return cache.addAll(ASSETS_TO_CACHE);
      })
      .then(() => self.skipWaiting())
  );
});

// Aktiviere den neuen Service Worker
self.addEventListener('activate', event => {
  const cacheAllowlist = [CACHE_NAME];

  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheAllowlist.indexOf(cacheName) === -1) {
            // Lösche alte Caches
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// Netzwerkanfragen abfangen
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // Cache Hit - Gib die gespeicherte Antwort zurück
        if (response) {
          return response;
        }

        // Kein Cache Hit - Hole vom Netzwerk
        return fetch(event.request).then(
          response => {
            // Prüfe, ob wir eine gültige Antwort bekommen haben
            if(!response || response.status !== 200 || response.type !== 'basic') {
              return response;
            }

            // Klone die Antwort, da der Body nur einmal gelesen werden kann
            const responseToCache = response.clone();

            caches.open(CACHE_NAME)
              .then(cache => {
                cache.put(event.request, responseToCache);
              });

            return response;
          }
        );
      })
  );
}); 
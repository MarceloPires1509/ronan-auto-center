// Service Worker Básico para permitir instalação do PWA
const CACHE_NAME = 'ronan-pwa-v1';

self.addEventListener('install', (event) => {
    self.skipWaiting();
});

self.addEventListener('activate', (event) => {
    event.waitUntil(clients.claim());
});

self.addEventListener('fetch', (event) => {
    // Apenas repassa as requisições (necessário para o Chrome aceitar instalar como App)
    event.respondWith(
        fetch(event.request).catch(() => {
            // Se falhar (offline), o Chrome ao menos tentará resolver
            return new Response("Você está offline.");
        })
    );
});

// serviceWorkerRegistration.js

export function register() {
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
      navigator.serviceWorker.register('/service-worker.js').then(registration => {
        console.log('Service Worker registrato con successo:', registration);
      }).catch(error => {
        console.error('Registrazione Service Worker fallita:', error);
      });
    });
  }
}

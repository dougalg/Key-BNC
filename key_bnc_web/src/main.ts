import { createApp } from 'vue'
import App from './App.vue'
import { polyfillDialogIfNeeded } from './polyfills/dialog'

const run = async () => {
	await polyfillDialogIfNeeded();
	createApp(App).mount('#app')
};

run();

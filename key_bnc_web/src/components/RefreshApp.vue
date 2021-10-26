<template>
	<transition name="slide">
		<div
			v-if="state.updateExists"
			class="refresh-alert"
		>
			New content is available.
			<basic-button @click="refreshApp">
				Refresh page
			</basic-button>
		</div>
	</transition>
</template>

<script setup lang="ts">
import { onMounted } from '@vue/runtime-core'
import BasicButton from '@/components/buttons/BasicButton.vue'
import { registerSW } from 'virtual:pwa-register'

const state = {
	refreshing: false,
	updateExists: false,
	registration: undefined as ServiceWorkerRegistration | undefined,
}

const updateSW = registerSW({
	onNeedRefresh() {
		state.updateExists = true
	},
	onOfflineReady() {
		console.log('offline ready')
	},
})

const showRefreshUI = (e: Event) => {
	if ('detail' in e) {
		state.registration = (e as CustomEvent).detail
		state.updateExists = true
	}
}

onMounted(() => {
	document.addEventListener('swUpdated', showRefreshUI, { once: true })
	navigator.serviceWorker.addEventListener('controllerchange', () => {
		if (state.refreshing) {
			return
		}
		state.refreshing = true
		window.location.reload()
	})
})

const refreshApp = () => {
	updateSW()
	state.updateExists = false
}
</script>

<style lang="scss" scoped>
.refresh-alert {
	position: absolute;
	padding: 0.5rem 1rem;
	top: 0;
	left: 0;
	right: 0;
	background-color: rgb(255 255 255 / 90%);
	transform: translateY(0);
	transition: transform 0.5s;
	z-index: 1000000;
}

.slide-enter,
.slide-leave-to {
	transform: translateY(-100%);
}
</style>

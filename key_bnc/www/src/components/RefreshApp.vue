<template>
	<transition name="slide">
		<div
			v-if="updateExists"
			class="refresh-alert"
		>
			New content is available.
			<basic-button @click="refreshApp">
				Refresh page
			</basic-button>
		</div>
	</transition>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import BasicButton from '@/components/buttons/BasicButton.vue'

@Component({ components: { BasicButton } })
export default class RefreshApp extends Vue {
	refreshing = false
	updateExists = false
	registration: ServiceWorkerRegistration | undefined = undefined

	created () {
		document.addEventListener('swUpdated', this.showRefreshUI, { once: true })
		navigator.serviceWorker.addEventListener('controllerchange', () => {
			if (this.refreshing) return
			this.refreshing = true
			window.location.reload()
		})
	}

	showRefreshUI (e: Event) {
		if ('detail' in e) {
			this.registration = (e as CustomEvent).detail
			this.updateExists = true
		}
	}

	refreshApp () {
		this.updateExists = false
		if (!this.registration || !this.registration.waiting) {
			return
		}
		this.registration.waiting.postMessage({ type: 'SKIP_WAITING' })
	}
}
</script>

<style lang="scss" scoped>
.refresh-alert {
	position: absolute;
	padding: 0.5rem 1rem;
	top: 0;
	left: 0;
	right: 0;
	background-color: rgba(255, 255, 255, 0.9);
	transform: translateY(0);
	transition: transform 0.5s;
}

.slide-enter,
.slide-leave-to {
	transform: translateY(-100%);
}
</style>

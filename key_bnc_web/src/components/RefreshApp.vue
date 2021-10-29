<template>
	<transition name="slide">
		<div
			v-if="state.updateExists"
			class="refresh-alert"
		>
			New content is available.
			<basic-button
				class="refresh-button"
				@click="refreshApp"
			>
				Refresh page
			</basic-button>
		</div>
		<div
			v-else-if="state.offlineReady"
			class="refresh-alert"
		>
			<div class="offline-mode">
				<p>
					Ready to work offline
				</p>
				<p class="note">
					(You are now ready visit this website without internet)
				</p>
			</div>
			<basic-button
				class="refresh-button"
				@click="clearOfflineReady"
			>
				OK
			</basic-button>
		</div>
	</transition>
</template>

<script setup lang="ts">
import BasicButton from '@/components/buttons/BasicButton.vue'
import { reactive } from '@vue/reactivity'
import { registerSW } from 'virtual:pwa-register'

const state = reactive({
	updateExists: false,
	offlineReady: false,
	registration: undefined as ServiceWorkerRegistration | undefined,
})

const updateSW = registerSW({
	onNeedRefresh() {
		state.updateExists = true
	},
	onOfflineReady() {
		state.offlineReady = true
	},
})

const refreshApp = () => {
	updateSW()
	state.updateExists = false
}

const clearOfflineReady = () => {
	state.offlineReady = false
}
</script>

<style lang="scss" scoped>
.refresh-alert {
	display: flex;
	align-items: center;
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

.refresh-button:not(:hover):not(:focus) {
	border-color: #999;
}

.offline-mode {
	display: flex;
	flex-direction: column;
	margin-inline-end: 2rem;

	& > * {
		margin: 0;
		padding: 0;
	}
}

.note {
	font-size: 1rem;
}
</style>

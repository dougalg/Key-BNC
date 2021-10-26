<script setup lang="ts">
import { computed, onMounted, reactive } from '@vue/runtime-core'
import init, { KeyBnc } from 'key_bnc_wasm'
import KeyBncInterface from './components/Interface.vue'
import BncLoader from './components/BncLoader.vue'
import RefreshApp from './components/RefreshApp.vue'

const state = reactive({
	keyBnc: null as KeyBnc | null,
	hasLoadedBncData: false,
})

const version = __APP_VERSION__;

const pollBncCsv = () => {
	const pollFn = () => {
		state.hasLoadedBncData = state.keyBnc !== null
			&& state.keyBnc.get_has_loaded_bnc_data()

		if (!state.hasLoadedBncData) {
			window.setTimeout(pollFn, 20)
		}
	}
	window.setTimeout(pollFn, 20)
}

onMounted(async () => {
	const csvImport = import('@virtual:plain-text/src/assets/BNC_wordlist.csv').then((_) => _.plainText)
	await init();
	state.keyBnc = KeyBnc.new()
	const csv = await csvImport
	state.keyBnc.load_bnc_data(csv)
	pollBncCsv()
})

const isReady = computed(() => Boolean(state.keyBnc) && state.hasLoadedBncData)
</script>

<template>
	<main id="app">
		<refresh-app />
		<transition
			name="fade"
			mode="out-in"
		>
			<key-bnc-interface
				v-if="isReady && state.keyBnc"
				:key-bnc="state.keyBnc"
			/>
			<bnc-loader v-else />
		</transition>

		<transition name="fade">
			<div
				v-if="isReady"
				class="version"
			>
				<p>{{ version }}</p>
				<img
					class="logo"
					src="@/assets/key-bnc-logo-white-225x278.png"
					alt="A black key on a white backgorund"
				>
			</div>
		</transition>
	</main>
</template>

<style lang="scss">
*,
*::before,
*::after {
	box-sizing: border-box;
}

html {
	font-size: 62.5%;
}

html,
body {
	margin: 0;
	padding: 0;
}

#app {
	font-family: Avenir, Helvetica, Arial, sans-serif;
	-webkit-font-smoothing: antialiased;
	-moz-osx-font-smoothing: grayscale;
	font-size: 1.6rem;
}

button {
	appearance: none;
	border: none;
	padding: 1rem 2rem;
	margin: 0;
	text-decoration: none;
	background: white;
	color: black;
	text-align: center;
	cursor: pointer;
}

.no-outline {
	outline: none !important;
	-webkit-tap-highlight-color: transparent !important;

	&::-moz-focus-inner {
		border: 0 !important;
	}
}

.version {
	position: absolute;
	display: flex;
	flex-direction: column;
	align-items: center;
	top: 0.5rem;
	right: 0.5rem;
	color: white;
	padding: 0;
	margin: 0;
	font-size: 1.2rem;

	& p {
		margin: 0;
	}
}

.logo {
	height: 5rem;
}

.fade-enter,
.fade-leave-to {
	opacity: 0%;
}

.fade-enter-to,
.fade-leave {
	opacity: 100%;
}

.fade-enter-active {
	transition: opacity 0.5s;
}
</style>

<script setup lang="ts">
import { computed, onMounted, reactive } from "vue";
import init, { KeyBnc } from "key_bnc_wasm";
import KeyBncInterface from "./components/AppInterface.vue";
import BncLoader from "./components/BncLoader.vue";
import RefreshApp from "./components/RefreshApp.vue";
import ChangelogModal from "./components/changelog/ChangelogModal.vue";

const state = reactive({
	keyBnc: null as KeyBnc | null,
	hasLoadedBncData: false,
	isChangelogModalOpen: false,
});

// eslint-disable-next-line no-undef
const version = __APP_VERSION__;

const pollBncCsv = () => {
	const pollFn = () => {
		// console.log(state.keyBnc, state.keyBnc?.get_has_loaded_bnc_data());
		state.hasLoadedBncData
			= state.keyBnc !== null && state.keyBnc.get_has_loaded_bnc_data();

		if (!state.hasLoadedBncData) {
			window.setTimeout(pollFn, 20);
		}
	};
	window.setTimeout(pollFn, 20);
};

onMounted(async () => {
	const csvImport
		= import("@virtual:plain-text/src/assets/BNC_wordlist.csv").then(
			(_) => _.default,
		);
	await init();
	state.keyBnc = KeyBnc.new();
	const csv = await csvImport;
	state.keyBnc.load_bnc_data(csv);
	pollBncCsv();
});

const isReady = computed(() => Boolean(state.keyBnc) && state.hasLoadedBncData);
</script>

<template>
	<main id="app">
		<refresh-app />
		<changelog-modal
			:open="state.isChangelogModalOpen"
			:version="version"
			@close="state.isChangelogModalOpen = false"
		/>

		<transition name="fade">
			<button
				v-if="isReady"
				class="version"
				@click="state.isChangelogModalOpen = true"
			>
				<p>{{ version }}</p>
				<span class="sr-only">View changelog</span>
				<img
					class="logo"
					src="@/assets/key-bnc-logo-white-225x278.png"
					alt="A black key on a white backgorund"
				>
			</button>
		</transition>
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

.sr-only {
	position:absolute;
	left:-10000px;
	top:auto;
	width:1px;
	height:1px;
	overflow:hidden;
}

.no-outline {
	outline: none !important;
	-webkit-tap-highlight-color: transparent !important;

	&::-moz-focus-inner {
		border: 0 !important;
	}
}

.version {
	all: unset;
	position: absolute;
	display: flex;
	flex-direction: column;
	align-items: center;
	top: 0.5rem;
	right: 0.5rem;
	color: white;
	padding: 2px;
	margin: 0;
	font-size: 1.2rem;

	& p {
		margin: 0;
	}
}

.version:focus-visible,
.version:hover {
	outline: 2px solid white;
	border-radius: 2px;
	cursor: pointer;
}

.logo {
	height: 5rem;
}

.fade-enter,
.fade-leave-to {
	opacity: 0;
}

.fade-enter-to,
.fade-leave {
	opacity: 1;
}

.fade-enter-active {
	transition: opacity 0.5s;
}
</style>

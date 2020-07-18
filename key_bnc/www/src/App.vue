<template>
	<main id="app">
		<refresh-app />
		<key-bnc-interface
			v-if="isReady"
			:key-bnc="keyBnc"
		/>
		<bnc-loader v-else />

		<div class="version">
			<p>{{ version }}</p>
			<img
				class="logo"
				src="@/assets/key-bnc-logo-white-225x278.png"
				alt="A black key on a white backgorund"
			/>
		</div>
	</main>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { KeyBnc } from '../../pkg/key_bnc'
import KeyBncInterface from '@/components/Interface.vue'
import BncLoader from '@/components/BncLoader.vue'
import RefreshApp from '@/components/RefreshApp.vue'

@Component({ components: { KeyBncInterface, BncLoader, RefreshApp } })
export default class App extends Vue {
	keyBnc: KeyBnc | null = null
	hasLoadedBncData = false
	tid = -1
	version = process.env.VUE_APP_VERSION

	mounted () {
		const csvImport = import('./assets/BNC_wordlist.csv').then((_) => _.default)
		import('../../pkg/key_bnc.js')
			.then(({ KeyBnc }) => {
				this.keyBnc = KeyBnc.new()
				return this.keyBnc
			})
			.then((keyBnc) => {
				csvImport.then((csv) => {
					keyBnc.load_bnc_data(csv)
					this.pollBncCsv()
				})
			})
	}

	pollBncCsv () {
		const pollFn = () => {
			this.hasLoadedBncData = this.keyBnc !== null
				&& this.keyBnc.get_has_loaded_bnc_data()

			if (!this.hasLoadedBncData) {
				window.setTimeout(pollFn, 20)
			}
		}
		window.setTimeout(pollFn, 20)
	}

	get isReady (): boolean {
		return Boolean(this.keyBnc)
			&& this.hasLoadedBncData
	}
}
</script>

<style lang="scss">
*,
*:before,
*:after {
	box-sizing: border-box
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
	-webkit-appearance: none;
	-moz-appearance: none;
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
</style>

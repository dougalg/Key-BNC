<template>
	<div id="app">
		<key-bnc-interface
			v-if="isReady"
			:key-bnc="keyBnc"
		/>
	</div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { KeyBnc } from '../../pkg/key_bnc'
import KeyBncInterface from '@/components/Interface.vue'

@Component({ components: { KeyBncInterface } })
export default class App extends Vue {
	keyBnc: KeyBnc | null = null
	hasLoadedBncData = false
	tid = -1

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

	isReady (): boolean {
		return Boolean(this.keyBnc)
			&& this.hasLoadedBncData
	}
}
</script>

<style lang="scss">
#app {
	font-family: Avenir, Helvetica, Arial, sans-serif;
	-webkit-font-smoothing: antialiased;
	-moz-osx-font-smoothing: grayscale;
	text-align: center;
}
</style>

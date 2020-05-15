<template>
	<div id="app">
		<key-bnc-interface
			v-if="keyBnc"
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

	mounted () {
		import('../../pkg/key_bnc.js')
			.then(({ KeyBnc }) => {
				this.keyBnc = KeyBnc.new()
			})
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

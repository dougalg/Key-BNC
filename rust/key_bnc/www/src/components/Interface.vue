<template>
	<div>
		<input
			ref="input"
			type="file"
			multiple
			@change="onFileChange"
		/>
		<button @click="updateStats">
			Update Stats
		</button>
	</div>
</template>

<script lang="ts">
import { Component, Prop, Vue, Ref } from 'vue-property-decorator'
import { KeyBnc } from '../../../pkg/key_bnc'

@Component
export default class HelloWorld extends Vue {
	@Ref() readonly input!: HTMLInputElement
	@Prop() private keyBnc!: KeyBnc

	onFileChange () {
		if (this.input.files === null) {
			return
		}

		for (let i = 0; i < this.input.files.length; i++) {
			const f = this.input.files[i]
			if (f !== null) {
				this.processFile(f)
			}
		}
	}

	processFile (f: File) {
		const fileReader = new FileReader()
		fileReader.onloadend = () => {
			const someId = this.keyBnc.add_entry(fileReader)
			console.log(this.keyBnc.get_token_count(), someId)
		}
		fileReader.readAsText(f)
	}

	updateStats () {
		console.log(this.keyBnc.get_stats())
	}
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>

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
		<table>
			<tr>
				<th>Word</th>
				<th>Count</th>
				<th>Log Likelyhood</th>
				<th>Odds Ratio</th>
				<th>Dispersion</th>
			</tr>
			<tr
				v-for="d in data"
				:key="d.word"
			>
				<td>{{ d.word }}</td>
				<td>{{ d.count }}</td>
				<td>{{ trunc(d.log_likelyhood) }}</td>
				<td>{{ formatOr(d.odds_ratio) }}</td>
				<td>{{ trunc(d.dispersion) }}</td>
			</tr>
		</table>
	</div>
</template>

<script lang="ts">
import { Component, Prop, Vue, Ref } from 'vue-property-decorator'
import { KeyBnc } from '../../../pkg/key_bnc'

const MAX_ITEMS = 1000

interface WordStats {
	word: string;
	count: number;
	log_likelyhood: number;
	odds_ratio: number;
	dispersion: number;
}

@Component
export default class HelloWorld extends Vue {
	@Ref() readonly input!: HTMLInputElement
	@Prop() private keyBnc!: KeyBnc

	data: Array<WordStats> = []

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
		const data = (this.keyBnc.get_stats() as Array<WordStats>)
			.sort((a, b) => b.count - a.count)
		data.splice(MAX_ITEMS)
		this.data = data
	}

	formatOr (n: number | null) {
		if (n == null) {
			return '∞'
		}
		return this.trunc(n)
	}

	trunc (n: number) {
		return n.toFixed(4)
	}
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
tr > td {
	text-align: left;
}
tr > td:nth-child(2) {
	text-align: right;
}
</style>

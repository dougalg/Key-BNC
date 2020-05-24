<template>
	<div>
		<h2>Statistics</h2>
		<div v-if="wordStats.length < 1">
			No data loaded. Load some files for your corpus to get started.
		</div>
		<table v-else>
			<tr>
				<th>Word Type</th>
				<th>Frequency</th>
				<th>Frequency BNC</th>
				<th>Log Likelyhood</th>
				<th>Odds Ratio</th>
				<th>Dispersion</th>
			</tr>
			<tr
				v-for="d in wordStats"
				:key="d.word"
			>
				<td>{{ d.word }}</td>
				<td>{{ d.frequency }}</td>
				<td>{{ d.frequency_bnc }}</td>
				<td>{{ trunc(d.log_likelyhood) }}</td>
				<td>{{ formatOddsRatio(d.odds_ratio) }}</td>
				<td>{{ trunc(d.dispersion) }}</td>
			</tr>
		</table>
	</div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'

@Component
export default class WordStats extends Vue {
	@Prop() wordStats!: Array<WordStats>

	formatOddsRatio (n: number | null) {
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
tr > td:nth-child(2),
tr > td:nth-child(3) {
	text-align: right;
}
</style>

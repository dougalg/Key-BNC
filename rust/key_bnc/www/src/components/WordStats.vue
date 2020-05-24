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
				<td>{{ numberFormat(d.frequency) }}</td>
				<td>{{ numberFormat(d.frequency_bnc) }}</td>
				<td>{{ numberFormat4(d.log_likelyhood) }}</td>
				<td>{{ formatOddsRatio(d.odds_ratio) }}</td>
				<td>{{ numberFormat4(d.dispersion) }}</td>
			</tr>
		</table>
	</div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'

const formatter = (Intl && Intl.NumberFormat)
	? new Intl.NumberFormat('en-CA')
	: { format (n: number) { return n.toString() } }

const formatter4 = (Intl && Intl.NumberFormat)
	? new Intl.NumberFormat('en-CA', { minimumFractionDigits: 4, maximumFractionDigits: 4 })
	: { format (n: number) { return n.toFixed(4) } }

@Component
export default class WordStats extends Vue {
	@Prop() wordStats!: Array<WordStats>

	formatOddsRatio (n: number | null): string {
		if (n == null) {
			return '∞'
		}
		return this.numberFormat4(n)
	}

	numberFormat (n: number): string {
		return formatter.format(n)
	}

	numberFormat4 (n: number): string {
		return formatter4.format(n)
	}
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
tr > td {
	text-align: right;
}
tr > td:first-child {
	text-align: left;
}
</style>

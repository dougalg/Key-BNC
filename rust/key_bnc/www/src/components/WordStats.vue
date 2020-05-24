<template>
	<div>
		<h2>Statistics</h2>
		<div v-if="wordStats.length < 1">
			No data loaded. Load some files for your corpus to get started.
		</div>
		<table v-else>
			<thead>
				<tr>
					<th>Word Type</th>
					<th>
						<sort-button
							:sort="getSortDirectionFor(SortBy.FREQUENCY)"
							@click="setSort(SortBy.FREQUENCY)"
						>
							Frequency
						</sort-button>
					</th>
					<th>
						<sort-button
							:sort="getSortDirectionFor(SortBy.FREQUENCY_BNC)"
							@click="setSort(SortBy.FREQUENCY_BNC)"
						>
							Frequency BNC
						</sort-button>
					</th>
					<th>
						<sort-button
							:sort="getSortDirectionFor(SortBy.LL)"
							@click="setSort(SortBy.LL)"
						>
							Log Likelyhood
						</sort-button>
					</th>
					<th>
						<sort-button
							:sort="getSortDirectionFor(SortBy.OR)"
							@click="setSort(SortBy.OR)"
						>
							Odds Ratio
						</sort-button>
					</th>
					<th>
						<sort-button
							:sort="getSortDirectionFor(SortBy.DISPERSION)"
							@click="setSort(SortBy.DISPERSION)"
						>
							Dispersion
						</sort-button>
					</th>
				</tr>
			</thead>
			<tbody>
				<tr
					v-for="d in sortedStats"
					:key="d.word"
				>
					<td>{{ d.word }}</td>
					<td>{{ numberFormat(d.frequency) }}</td>
					<td>{{ numberFormat(d.frequency_bnc) }}</td>
					<td>{{ numberFormat4(d.log_likelyhood) }}</td>
					<td>{{ formatOddsRatio(d.odds_ratio) }}</td>
					<td>{{ numberFormat4(d.dispersion) }}</td>
				</tr>
			</tbody>
		</table>
	</div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'
import { WordStats, SortBy, SortDirection } from '../models'
import SortButton from './SortButton.vue'

const SORTERS_ASC = {
	[SortBy.FREQUENCY]: (a: WordStats, b: WordStats) => a.frequency - b.frequency,
	[SortBy.FREQUENCY_BNC]: (a: WordStats, b: WordStats) => a.frequency_bnc - b.frequency_bnc,
	[SortBy.LL]: (a: WordStats, b: WordStats) => a.log_likelyhood - b.log_likelyhood,
	[SortBy.OR]: (a: WordStats, b: WordStats) => a.odds_ratio - b.odds_ratio,
	[SortBy.DISPERSION]: (a: WordStats, b: WordStats) => a.dispersion - b.dispersion,
}

const SORTERS_DESC = {
	[SortBy.FREQUENCY]: (a: WordStats, b: WordStats) => b.frequency - a.frequency,
	[SortBy.FREQUENCY_BNC]: (a: WordStats, b: WordStats) => b.frequency_bnc - a.frequency_bnc,
	[SortBy.LL]: (a: WordStats, b: WordStats) => b.log_likelyhood - a.log_likelyhood,
	[SortBy.OR]: (a: WordStats, b: WordStats) => b.odds_ratio - a.odds_ratio,
	[SortBy.DISPERSION]: (a: WordStats, b: WordStats) => b.dispersion - a.dispersion,
}

const formatter = (Intl && Intl.NumberFormat)
	? new Intl.NumberFormat('en-CA')
	: { format (n: number) { return n.toString() } }

const formatter4 = (Intl && Intl.NumberFormat)
	? new Intl.NumberFormat('en-CA', { minimumFractionDigits: 4, maximumFractionDigits: 4 })
	: { format (n: number) { return n.toFixed(4) } }

@Component({ components: { SortButton } })
export default class WordStatsView extends Vue {
	@Prop() wordStats!: Array<WordStats>
	private SortBy = SortBy
	private currentSort: SortBy = SortBy.FREQUENCY
	private currentSortDirection: SortDirection = SortDirection.DESC

	get sortedStats (): Array<WordStats> {
		const sortFn = this.currentSortDirection === SortDirection.ASC
			? SORTERS_ASC[this.currentSort]
			: SORTERS_DESC[this.currentSort]
		return this.wordStats
			.sort(sortFn)
	}

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

	setSort (newSort: SortBy): void {
		if (this.currentSort === newSort) {
			this.currentSortDirection = this.currentSortDirection === SortDirection.ASC
				? SortDirection.DESC
				: SortDirection.ASC
		} else {
			this.currentSort = newSort
			this.currentSortDirection = SortDirection.DESC
		}
	}

	getSortDirectionFor (sort: SortBy): SortDirection {
		if (this.currentSort === sort) {
			return this.currentSortDirection
		}
		return SortDirection.NONE
	}
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
table {
	border-spacing: 1rem 0.5rem;
}
thead {
	position: sticky;
	top: 0;
	background: white;
	box-shadow: 0px 3px black;
}
tr > td {
	text-align: right;
}
tr > td:first-child {
	text-align: left;
}
</style>

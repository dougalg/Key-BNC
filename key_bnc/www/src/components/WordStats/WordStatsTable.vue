<template>
	<table>
		<thead>
			<tr>
				<th>{{ headerText.word }}</th>
				<th>
					<sort-button
						:sort="getSortDirectionFor(SortBy.FREQUENCY)"
						@click="$emit('set-sort', SortBy.FREQUENCY)"
					>
						{{ headerText.frequency }}
					</sort-button>
				</th>
				<th>
					<sort-button
						:sort="getSortDirectionFor(SortBy.FREQUENCY_BNC)"
						@click="$emit('set-sort', SortBy.FREQUENCY_BNC)"
					>
						{{ headerText.frequency_bnc }}
					</sort-button>
				</th>
				<th>
					<sort-button
						:sort="getSortDirectionFor(SortBy.LL)"
						@click="$emit('set-sort', SortBy.LL)"
					>
						{{ headerText.log_likelihood }}
					</sort-button>
				</th>
				<th>
					<sort-button
						:sort="getSortDirectionFor(SortBy.OR)"
						@click="$emit('set-sort', SortBy.OR)"
					>
						{{ headerText.odds_ratio }}
					</sort-button>
				</th>
				<th>
					<sort-button
						:sort="getSortDirectionFor(SortBy.DISPERSION)"
						@click="$emit('set-sort', SortBy.DISPERSION)"
					>
						{{ headerText.dispersion }}
					</sort-button>
				</th>
			</tr>
		</thead>
		<tbody>
			<tr
				v-for="d in words"
				:key="d.word"
			>
				<td>{{ d.word }}</td>
				<td>{{ numberFormat(d.frequency) }}</td>
				<td>{{ numberFormat(d.frequency_bnc) }}</td>
				<td>{{ numberFormat4(d.log_likelihood) }}</td>
				<td>{{ formatOddsRatio(d.odds_ratio) }}</td>
				<td>{{ numberFormat4(d.dispersion) }}</td>
			</tr>
		</tbody>
	</table>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'
import { WordStats, SortBy, SortDirection } from '@/models'
import { WORD_STAT_HEADERS } from '@/lang/wordStats'
import SortButton from './SortButton.vue'
import StatFilters from './StatFilters.vue'

const formatter = (Intl && Intl.NumberFormat)
	? new Intl.NumberFormat('en-CA')
	: { format (n: number) { return n.toString() } }

const formatter4 = (Intl && Intl.NumberFormat)
	? new Intl.NumberFormat('en-CA', { minimumFractionDigits: 4, maximumFractionDigits: 4 })
	: { format (n: number) { return n.toFixed(4) } }

@Component({ components: { SortButton, StatFilters } })
export default class WordStatsView extends Vue {
	@Prop() words!: Array<WordStats>
	@Prop() sortBy!: SortBy
	@Prop() sortDirection!: SortDirection
	private SortBy = SortBy
	private headerText = WORD_STAT_HEADERS

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

	getSortDirectionFor (sort: SortBy): SortDirection {
		if (this.sortBy === sort) {
			return this.sortDirection
		}
		return SortDirection.NONE
	}
}
</script>

<style scoped lang="scss">
table,
thead,
tbody {
	$horiz-space: 1rem;
	border-spacing: $horiz-space 0.5rem;
	margin-left: -$horiz-space;
	margin-right: -$horiz-space;
	height: max-content
}
thead {
	position: sticky;
	top: 0;
	background: white;
	box-shadow: 0px 3px black;
}
th {
	padding: 0;
}
tr > td {
	text-align: right;
}
tr > td:first-child {
	text-align: left;
}
</style>

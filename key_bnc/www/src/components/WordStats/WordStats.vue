<template>
	<div class="word-stats">
		<div class="stats-header">
			<h2>Statistics</h2>
			<stat-filters
				v-if="wordStats.length > 0"
				:filters="filters"
				@add-filter="addFilter"
				@filter-change="updateFilter"
				@remove-filter="removeFilter"
			/>
		</div>
		<div v-if="wordStats.length < 1">
			No data loaded. Load some files for your corpus to get started.
		</div>
		<word-stats-table
			v-else
			:words="sortedFilteredStats"
			:sort-by="currentSort"
			:sort-direction="currentSortDirection"
			@set-sort="setSort"
		/>
	</div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'
import {
	WordStats,
	SortBy,
	SortDirection,
	FilterType,
} from '@/models'
import SortButton from './SortButton.vue'
import StatFilters from './StatFilters.vue'
import WordStatsTable from './WordStatsTable.vue'
import { getFrequencyFilter, getFrequencyBncFilter, getLlFilter, getOrFilter, getDispersionFilter, Filter, FilterProps } from './filters'

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

const FilterGetters = {
	[FilterType.FREQUENCY]: getFrequencyFilter,
	[FilterType.FREQUENCY_BNC]: getFrequencyBncFilter,
	[FilterType.LL]: getLlFilter,
	[FilterType.OR]: getOrFilter,
	[FilterType.DISPERSION]: getDispersionFilter,
}

@Component({ components: { SortButton, StatFilters, WordStatsTable } })
export default class WordStatsView extends Vue {
	@Prop() wordStats!: Array<WordStats>
	private SortBy = SortBy
	private currentSort: SortBy = SortBy.FREQUENCY
	private currentSortDirection: SortDirection = SortDirection.DESC
	private filters: Filter[] = []

	get sortedFilteredStats (): Array<WordStats> {
		const sortFn = this.currentSortDirection === SortDirection.ASC
			? SORTERS_ASC[this.currentSort]
			: SORTERS_DESC[this.currentSort]
		return this.wordStats
			.filter((val) => {
				if (this.filters.length === 0) {
					return true
				}
				return this.filters.every((filter) => filter.test(val))
			})
			.sort(sortFn)
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

	addFilter (filterType: FilterType): void {
		this.filters.push(FilterGetters[filterType]())
	}

	updateFilter (targetId: string, props: FilterProps): void {
		const targetFilter = this.filters.find(({ id }) => targetId === id)
		if (!targetFilter) {
			console.error('Could not locate filter to update with id:', targetId)
		} else {
			targetFilter.props = props
		}
	}

	removeFilter (targetId: string) {
		this.filters = this.filters.filter(({ id }) => id !== targetId)
	}
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
table,
thead,
tbody {
	$horiz-space: 1rem;
	border-spacing: $horiz-space 0.5rem;
	margin-left: -$horiz-space;
	margin-right: -$horiz-space;
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

.word-stats {
	display: grid;
}

.stats-header {
	display: flex;
	align-items: center;
	justify-content: space-between;
}
</style>

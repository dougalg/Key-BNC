<template>
	<div class="word-stats">
		<div class="stats-header">
			<h2 class="heading">
				Statistics
			</h2>
			<stat-filters
				v-if="wordStats.length > 0"
				:filters="filters"
				:open-filter-dropdown="openFilterDropdown"
				@toggle-filter-dropdown="toggleFilterDropdown"
				@add-filter="addFilter"
				@filter-change="updateFilter"
				@remove-filter="removeFilter"
			/>
			<basic-button
				v-if="wordStats.length > 0"
				@click="downloadCsv"
			>
				Export CSV
			</basic-button>
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
import {
	WordStats,
	SortBy,
	SortDirection,
	FilterType,
} from '@/models'
import StatFilters from './StatFilters.vue'
import WordStatsTable from './WordStatsTable.vue'
import BasicButton from '@/components/buttons/BasicButton.vue'
import {
	getFrequencyFilter,
	getFrequencyBncFilter,
	getLlFilter,
	getOrFilter,
	getDispersionFilter,
	Filter,
	FilterProps,
} from './filters'
import { toCSV } from '@/services/csv'
import { computed, defineComponent, PropType, toRefs } from '@vue/runtime-core'

const SORTERS_ASC = {
	[SortBy.FREQUENCY]: (a: WordStats, b: WordStats) => a.frequency - b.frequency,
	[SortBy.FREQUENCY_BNC]: (a: WordStats, b: WordStats) => a.frequency_bnc - b.frequency_bnc,
	[SortBy.LL]: (a: WordStats, b: WordStats) => a.log_likelihood - b.log_likelihood,
	[SortBy.OR]: (a: WordStats, b: WordStats) => a.odds_ratio - b.odds_ratio,
	[SortBy.DISPERSION]: (a: WordStats, b: WordStats) => a.dispersion - b.dispersion,
}

const SORTERS_DESC = {
	[SortBy.FREQUENCY]: (a: WordStats, b: WordStats) => b.frequency - a.frequency,
	[SortBy.FREQUENCY_BNC]: (a: WordStats, b: WordStats) => b.frequency_bnc - a.frequency_bnc,
	[SortBy.LL]: (a: WordStats, b: WordStats) => b.log_likelihood - a.log_likelihood,
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

export default defineComponent({
	components: { StatFilters, WordStatsTable, BasicButton },
	props: {
		wordStats: {
			type: Array as PropType<WordStats[]>,
			required: true,
		},
	},
	setup (props) {
		const state = {
			currentSort: SortBy.FREQUENCY,
			currentSortDirection: SortDirection.DESC,
			filters: [] as Filter[],
			openFilterDropdown: null as string | null,
		}

		const sortedFilteredStats = computed(() => {
			const sortFn = state.currentSortDirection === SortDirection.ASC
				? SORTERS_ASC[state.currentSort]
				: SORTERS_DESC[state.currentSort]
			return props.wordStats
				.filter((val) => {
					if (state.filters.length === 0) {
						return true
					}
					return state.filters.every((filter) => filter.test(val))
				})
				.sort(sortFn)
		})

		const toggleFilterDropdown = (filterId: string) => {
			state.openFilterDropdown = state.openFilterDropdown === filterId ? null : filterId
		}

		const setSort = (newSort: SortBy): void => {
			if (state.currentSort === newSort) {
				state.currentSortDirection = state.currentSortDirection === SortDirection.ASC
					? SortDirection.DESC
					: SortDirection.ASC
			} else {
				state.currentSort = newSort
				state.currentSortDirection = SortDirection.DESC
			}
		}

		const addFilter = (filterType: FilterType): void => {
			const newFilter = FilterGetters[filterType]()
			state.filters.push(newFilter)
			state.openFilterDropdown = newFilter.id
		}

		const updateFilter = (targetId: string, props: FilterProps): void => {
			const targetFilter = state.filters.find(({ id }) => targetId === id)
			if (!targetFilter) {
				console.error('Could not locate filter to update with id:', targetId)
			} else {
				targetFilter.props = props
			}
		}

		const removeFilter = (targetId: string) => {
			state.filters = state.filters.filter(({ id }) => id !== targetId)
			if (state.openFilterDropdown === targetId) {
				state.openFilterDropdown = null
			}
		}

		const downloadCsv = () => {
			const filename = 'Key-BNC.csv'
			const element = document.createElement('a')
			const text = toCSV(sortedFilteredStats.value)
			element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text))
			element.setAttribute('download', filename)

			element.style.display = 'none'
			document.body.appendChild(element)

			element.click()

			document.body.removeChild(element)
		}

		return {
			...toRefs(state),
			SortBy,
			sortedFilteredStats,
			toggleFilterDropdown,
			addFilter,
			updateFilter,
			removeFilter,
			setSort,
			downloadCsv,
		}
	},
})
</script>

<style scoped lang="scss">
.heading {
	margin-right: auto;
}

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
	box-shadow: 0 3px black;
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

	&:deep(.basic-button) {
		margin-left: 1rem;
	}
}
</style>

<template>
	<div class="stats-filters">
		<component
			v-for="filter in filters"
			:key="filter.id"
			:is="filter.component"
			:name="getFilterName(filter.type)"
			v-bind="filter.props"
			@input="$emit('filter-change', filter.id, $event)"
			@remove-self="$emit('remove-filter', filter.id)"
		/>
		<dropdown
			class="stats-filters"
			:isOpen="isStatsDropdownOpen"
			@toggle="isStatsDropdownOpen = !isStatsDropdownOpen"
		>
			<template v-slot:button-content>
				Add Filter +
			</template>
			<template v-slot:dropdown-content>
				<basic-button
					v-for="{ type, text } in buttons"
					:key="type"
					@click="onSelection(type)"
				>
					{{ text }}
				</basic-button>
			</template>
		</dropdown>
	</div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator'
import { FilterType } from '@/models'
import Dropdown from '@/components/Dropdown.vue'
import BasicButton from '@/components/buttons/BasicButton.vue'
import { Filter } from './filters'

const buttons = [
	{
		type: FilterType.FREQUENCY,
		text: 'Frequency',
	},
	{
		type: FilterType.FREQUENCY_BNC,
		text: 'Frequency (BNC)',
	},
	{
		type: FilterType.LL,
		text: 'LL',
	},
	{
		type: FilterType.OR,
		text: 'OR',
	},
	{
		type: FilterType.DISPERSION,
		text: 'Dispersion',
	},
]

const FilterNames = {
	[FilterType.FREQUENCY]: 'Frequency',
	[FilterType.FREQUENCY_BNC]: 'Frequency (BNC)',
	[FilterType.LL]: 'LL',
	[FilterType.OR]: 'OR',
	[FilterType.DISPERSION]: 'Dispersion',
}

@Component({ components: { Dropdown, BasicButton } })
export default class StatFilers extends Vue {
	@Prop() filters!: Filter[]
	isStatsDropdownOpen = false
	buttons = buttons

	getFilterName (type: FilterType): string {
		return FilterNames[type]
	}

	onSelection (type: FilterType): void {
		if (!this.canAddFilter(type)) {
			return
		}
		this.isStatsDropdownOpen = false
		this.$emit('add-filter', type)
	}

	canAddFilter (filterType: FilterType): boolean {
		return !this.filters.find(({ type }) => type === filterType)
	}
}
</script>

<style lang="scss" scoped>
.stats-filters {
	display: flex;
}

.stats-filters > * + * {
	margin-left: 0.4rem;
}
</style>

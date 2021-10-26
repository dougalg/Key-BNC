<template>
	<div class="stats-filters">
		<component
			:is="filter.component"
			v-for="filter in filters"
			:key="filter.id"
			:name="getFilterName(filter.type)"
			:is-dropdown-open="filter.id === openFilterDropdown"
			v-bind="filter.props"
			@toggle="$emit('toggle-filter-dropdown', filter.id)"
			@input="$emit('filter-change', filter.id, $event)"
			@remove-self="$emit('remove-filter', filter.id)"
		/>
		<dropdown
			class="stats-filters"
			:is-open="id === openFilterDropdown"
			@toggle="$emit('toggle-filter-dropdown', id)"
		>
			<template #button-content>
				Add Filter
			</template>
			<template #dropdown-content>
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
import { FilterType } from '@/models'
import Dropdown from '@/components/Dropdown.vue'
import BasicButton from '@/components/buttons/BasicButton.vue'
import { Filter } from './filters'
import { v4 } from 'uuid'
import { defineComponent, PropType } from '@vue/runtime-core'

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

export default defineComponent({
	components: { Dropdown, BasicButton },
	props: {
		filters: {
			type: Array as PropType<Filter[]>,
			required: true,
		},
		openFilterDropdown: {
			type: String as PropType<string | null>,
			required: true,
		},
	},
	emits: [
		'toggle-filter-dropdown',
		'filter-change',
		'remove-filter',
		'add-filter',
	],
	setup (props, ctx) {
		const getFilterName = (type: FilterType): string => {
			return FilterNames[type]
		}

		const canAddFilter = (filterType: FilterType): boolean => !props.filters.find(({ type }) => type === filterType)

		const onSelection = (type: FilterType): void => {
			if (!canAddFilter(type)) {
				return
			}
			ctx.emit('add-filter', type)
		}

		return {
			buttons,
			id: v4(),
			getFilterName,
			onSelection,
		}
	},
})
</script>

<style lang="scss" scoped>
.stats-filters {
	display: flex;
}

.stats-filters > * + * {
	margin-left: 0.4rem;
}
</style>

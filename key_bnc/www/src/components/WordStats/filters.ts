import { v4 } from 'uuid'
import { FilterType, WordStats } from '@/models'
import MinMaxFilterVue from '@/components/WordStats/filters/MinMaxFilter.vue'
import { VueConstructor } from 'vue/types/umd'

export interface Filter {
	id: string;
	type: FilterType;
	component: VueConstructor<Vue>;
	props: FilterProps;
	test(target: WordStats): boolean;
};

// eslint-disable-next-line @typescript-eslint/no-empty-interface
export interface FilterProps {}

export interface MinMaxFilterProps extends FilterProps {
	min: number;
	max: number;
}

export interface MinMaxFilter extends Filter {
	props: MinMaxFilterProps;
}

const createMinMaxFilter = (type: FilterType, component: VueConstructor<Vue>): MinMaxFilter => {
	return {
		id: v4(),
		type,
		component,
		props: {
			min: 1,
			max: Infinity,
		},
		test (target: WordStats) {
			return target[type] >= this.props.min && target[type] <= this.props.max
		},
	}
}

export const getFrequencyFilter = () => createMinMaxFilter(FilterType.FREQUENCY, MinMaxFilterVue)
export const getFrequencyBncFilter = () => createMinMaxFilter(FilterType.FREQUENCY_BNC, MinMaxFilterVue)
export const getLlFilter = () => createMinMaxFilter(FilterType.LL, MinMaxFilterVue)
export const getOrFilter = () => createMinMaxFilter(FilterType.OR, MinMaxFilterVue)
export const getDispersionFilter = () => createMinMaxFilter(FilterType.DISPERSION, MinMaxFilterVue)

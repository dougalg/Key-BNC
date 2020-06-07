<template>
	<dropdown :isOpen="isDropdownOpen">
		<template v-slot:button>
			<basic-button
				is-attached
				@click="isDropdownOpen = !isDropdownOpen"
			>
				{{ min }} &lt;= {{ name }} &lt;= {{ readableMax }}
			</basic-button>
			<basic-button
				:aria-label="`Remove ${name} filter`"
				is-attached
				@click="$emit('remove-self')"
			>
				x
			</basic-button>
		</template>
		<template v-slot:dropdown-content>
			<div>
				<label :for="minId">
					Min:
				</label>
				<input
					:id="minId"
					type="number"
					:value="min"
					min="0"
					:max="max"
					@change="updateMin($event.target.value)"
				/>
				<br />
				<label :for="maxId">
					Max:
				</label>
				<input
					:id="maxId"
					type="number"
					:value="max"
					:min="min"
					@change="updateMax($event.target.value)"
				/>
			</div>
		</template>
	</dropdown>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator'
import { v4 } from 'uuid'
import { MinMaxFilterProps } from '../filters'
import Dropdown from '@/components/Dropdown.vue'
import BasicButton from '@/components/buttons/BasicButton.vue'

@Component({ components: { Dropdown, BasicButton } })
export default class StatFilers extends Vue {
	@Prop() name!: string;
	@Prop() min!: number;
	@Prop() max!: number;
	minId = `min_${v4()}`
	maxId = `max_${v4()}`
	isDropdownOpen = false

	get readableMax (): string {
		return this.max === Infinity ? '∞' : this.max.toString()
	}

	updateMin (min: number): void {
		this.emitUpdate(min, this.max)
	}

	updateMax (max: number): void {
		this.emitUpdate(this.min, max || Infinity)
	}

	emitUpdate (min: number, max: number): void {
		const newFilter: MinMaxFilterProps = { min, max }
		this.$emit('input', newFilter)
	}
}
</script>

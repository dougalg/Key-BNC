<template>
	<dropdown
		:isOpen="isDropdownOpen"
		:position="Position.CENTER"
	>
		<template v-slot:button>
			<basic-button
				is-attached
				@click="$emit('toggle')"
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
			<div class="input-row">
				<label :for="minId">
					Min:
				</label>
				<input
					class="input no-outline"
					type="number"
					min="0"
					:id="minId"
					:value="min"
					:max="max"
					size="6"
					@change="updateMin($event.target.value)"
				/>
			</div>
			<div class="input-row">
				<label :for="maxId">
					Max:
				</label>
				<input
					class="input no-outline"
					type="number"
					:id="maxId"
					:value="max"
					:min="min"
					size="6"
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
import { Position } from '@/components/DropdownPosition'
import Dropdown from '@/components/Dropdown.vue'
import BasicButton from '@/components/buttons/BasicButton.vue'

@Component({ components: { Dropdown, BasicButton } })
export default class StatFilers extends Vue {
	@Prop() name!: string
	@Prop() min!: number
	@Prop() max!: number
	@Prop() isDropdownOpen!: boolean
	minId = `min_${v4()}`
	maxId = `max_${v4()}`
	Position = Position

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

<style lang="scss" scoped>
.input-row {
	display: flex;

	> input {
		flex-grow: 1;
	}
}

.input {
	border: 0;
	text-align: right;
	font-weight: bold;
	font-size: 1.5rem;
	border-bottom: 2px solid white;
	&:hover,
	&:focus {
		border-bottom: 2px solid black;
	}
}
</style>

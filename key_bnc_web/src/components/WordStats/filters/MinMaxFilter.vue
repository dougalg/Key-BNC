<template>
	<dropdown
		:is-open="isDropdownOpen"
		:position="Position.CENTER"
	>
		<template #button>
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
		<template #dropdown-content>
			<div class="input-row">
				<label :for="minId">
					Min:
				</label>
				<input
					:id="minId"
					class="input no-outline"
					type="number"
					min="0"
					:value="min"
					:max="max"
					size="6"
					@change="updateMin(extractValue($event))"
				>
			</div>
			<div class="input-row">
				<label :for="maxId">
					Max:
				</label>
				<input
					:id="maxId"
					class="input no-outline"
					type="number"
					:value="max"
					:min="min"
					size="6"
					@change="updateMax(extractValue($event))"
				>
			</div>
		</template>
	</dropdown>
</template>

<script lang="ts">
import { v4 } from 'uuid'
import { MinMaxFilterProps } from '../filters'
import { Position } from '@/components/DropdownPosition'
import Dropdown from '@/components/Dropdown.vue'
import BasicButton from '@/components/buttons/BasicButton.vue'
import { computed, defineComponent } from '@vue/runtime-core'

const isInputElement = (el: EventTarget): el is HTMLInputElement => Boolean((el as HTMLInputElement).value);

export default defineComponent({
	components: { Dropdown, BasicButton },
	props: {
		name: {
			type: String,
			required: true,
		},
		min: {
			type: Number,
			required: true,
		},
		max: {
			type: Number,
			required: true,
		},
		isDropdownOpen: {
			type: Boolean,
			required: true,
		},
	},
	emits: ['input', 'remove-self', 'toggle'],
	setup (props, ctx) {
		const minId = `min_${v4()}`
		const maxId = `max_${v4()}`

		const readableMax = computed(() => props.max === Infinity ? '∞' : props.max.toString())

		const emitUpdate = (min: number, max: number): void => {
			const newFilter: MinMaxFilterProps = { min, max }
			ctx.emit('input', newFilter)
		}

		const updateMin = (min = 0): void => {
			emitUpdate(min, props.max)
		}

		const updateMax = (max = Infinity): void => {
			emitUpdate(props.min, max || Infinity)
		}

		const extractValue = (e: Event) => {
			if (!e.target || !isInputElement(e.target)) {
				return undefined;
			}
			return parseInt(e.target.value, 10)
		}

		return {
			Position,
			readableMax,
			updateMin,
			updateMax,
			minId,
			maxId,
			extractValue,
		}
	},
})
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

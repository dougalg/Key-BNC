<template>
	<button
		class="basic-button no-outline"
		@click="$emit('click')"
	>
		<slot />
	</button>
</template>

<style lang="scss" scoped>
.basic-button {
	border-radius: 5px;
	background-color: #eee;
	border: 2px solid #eee;
	&:hover,
	&:focus {
		border-color: #111;
	}
}
</style>

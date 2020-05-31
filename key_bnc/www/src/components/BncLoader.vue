<template>
	<div class="loader">
		<h2>Loading...</h2>
		<div class="spinner">
			<div class="bounce1"></div>
			<div class="bounce2"></div>
			<div class="bounce3"></div>
		</div>
	</div>
</template>

<style lang="scss" scoped>
.loader {
	display: flex;
	align-items: center;
	justify-content: center;
	flex-direction: column;

	min-height: 100vh;
}

.spinner {
	width: 70px;
	text-align: center;
}

.spinner > div {
	width: 18px;
	height: 18px;
	background-color: #333;

	border-radius: 100%;
	display: inline-block;
	animation: sk-bouncedelay 1.4s infinite ease-in-out both;
}

.spinner .bounce1 {
	animation-delay: -0.32s;
}

.spinner .bounce2 {
	animation-delay: -0.16s;
}

@keyframes sk-bouncedelay {
	0%, 80%, 100% {
		-webkit-transform: scale(0);
		transform: scale(0);
	} 40% {
		-webkit-transform: scale(1.0);
		transform: scale(1.0);
	}
}
</style>

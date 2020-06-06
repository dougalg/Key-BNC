<template>
	<div>
		<div class="top container">
			<header>
				<h1>Key-BNC</h1>
			</header>
			<nav>
				<div role="tablist" class="tab-nav">
					<nav-button
						:is-selected="currentTab === tabs.MANAGE_CORPUS"
						@click.native="currentTab = tabs.MANAGE_CORPUS"
					>
						Manage Corpus
					</nav-button>
					<nav-button
						:is-selected="currentTab === tabs.WORD_STATS"
						@click.native="showStatsView"
					>
						Corpus Statistics
					</nav-button>
					<nav-button
						:is-selected="currentTab === tabs.ABOUT"
						@click.native="currentTab = tabs.ABOUT"
					>
						About
					</nav-button>
				</div>
			</nav>
		</div>
		<div class="tab-container container">
			<manage-corpus
				v-show="currentTab === tabs.MANAGE_CORPUS"
				:key-bnc="keyBnc"
				@corpus-changed="setDirty"
			/>
			<word-stats-view
				v-show="currentTab === tabs.WORD_STATS"
				:word-stats="wordStats"
			/>
			<about-view
				v-show="currentTab === tabs.ABOUT"
			/>
		</div>
	</div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'
import { KeyBnc } from '../../../pkg/key_bnc'
import { WordStats } from '../models'
import ManageCorpus from './ManageCorpus.vue'
import WordStatsView from './WordStats.vue'
import NavButton from './NavButton.vue'
import AboutView from './About.vue'

const MAX_ITEMS = 1000

const components = {
	ManageCorpus,
	WordStatsView,
	NavButton,
	AboutView,
}

enum Tabs {
	ABOUT,
	WORD_STATS,
	MANAGE_CORPUS,
}

@Component({ components })
export default class Interface extends Vue {
	@Prop() private keyBnc!: KeyBnc
	private wordStats: Array<WordStats> = []
	private tabs = Tabs
	private currentTab: Tabs = Tabs.MANAGE_CORPUS
	private isDirty = false

	setDirty () {
		this.isDirty = true
	}

	showStatsView () {
		this.currentTab = Tabs.WORD_STATS
		if (this.isDirty) {
			this.isDirty = false
			this.updateStats()
		}
	}

	updateStats () {
		const wordStats = (this.keyBnc.get_stats() as Array<WordStats>)
			.sort((a, b) => b.frequency - a.frequency)
		wordStats.splice(MAX_ITEMS)
		this.wordStats = wordStats
	}
}
</script>

<style lang="scss" scoped>
.top,
.tab-nav {
	display: flex;
	align-items: flex-end;
}

h1 {
	font-size: 1.1em;
	margin: 0 2rem 0 0;
	position: relative;
	top: 2rem;
	font-variant: small-caps;
	pointer-events: none;

	@media (max-width: 620px) {
		font-size: 0.8em;
		top: 0;
		margin: 1rem 0 0 0;
	}
}

.top {
	top: 0;
	left: 0;
	padding: 0;
	max-width: 100%;
	background-color: #000;
	color: #fff;
	font-size: 3em;
	height: 2.85em;

	@media (max-width: 620px) {
		height: auto;
		flex-direction: column;
		align-items: flex-start;
		justify-content: end;
	}
}

.container {
	padding-left: 1rem;
	padding-right: 1rem;
}

.tab-nav {
	position: relative;
	font-size: 1.5rem;
	font-weight: bold;
}

.tab-nav::before {
	position: absolute;
	content: " ";
	width: 100%;
	bottom: 0;
	left: 0;
	border-bottom: 1px solid black;
}
</style>

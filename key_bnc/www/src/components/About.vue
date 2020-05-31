<template>
	<div class="about-container">

		<section class="about">
			<h1>What is this, and who is it useful for?</h1>

			<p>This application provides a simple interface for calculating comparative keyword statistics against a word list from the British National Corpus (BNC) for linguists without access to the BNC.</p>

			<p>Source code and technical details are available on <a href="http://github.com/dougalg/Key-BNC">GitHub</a>.</p>
		</section>

		<section class="keyword">
			<h1>What is a keyword?</h1>

			<p>A keyword is a word whose frequency is significantly higher (or lower) in a corpus of interest than in a reference corpus. Keywords let us see what words can be considered important words in a  given text.</p>

			<p>Log-likelihood (LL) and Odds Ratio (OR) are statistical calculations which generate keyness values based on frequency of occurrence and can be used to rank words.</p>
		</section>

		<section class="statistics">
			<h1>About the statistics</h1>

			<p>The rankings of words based on LL and OR are likely to be in a different sequence. LL highlights words which are relatively common in general use, while OR highlights more specialised words which are peculiar to a target corpus.</p>

			<h2>Log-likelihood (LL)</h2>
			<p>LL, is a probability statistic which compares the frequency of occurrence of words in two corpora. High LL suggests a great difference between the relative frequencies of a word based on the sizes of the two corpora. When the relative proportions of word occurrences are the same, words with higher absolute frequencies, which are most likely common words, tend to have higher LL. This explains why more common words are highlighted in keyword lists ranked by LL.</p>

			<h2>Odds ratio (OR)</h2>
			<p>OR is an effect size statistic which measures relative proportions of word frequencies in the target corpus and the reference corpus and suggests how much the difference is between the word frequencies in the two corpora. When the relative proportions are the same, more frequent words tend to have slightly lower OR than less frequent words. Therefore, OR, is likely to rank less common words near the top of keyword lists.</p>
		</section>

		<section class="references">
			<h1>Some references</h1>

			<h2>Online LL wizard:</h2>

			<p class="reference">Rayson, P. 2008b: online. Log-likelihood calculator. UCREL web server. Available at: <a href="http://ucrel.lancs.ac.uk/llwizard.html">http://ucrel.lancs.ac.uk/llwizard.html</a></p>

			<h2>Online OR wizard:</h2>

			<p class="reference">"Odds Ratio." Odds Ratio Calculator. MedCalc Software, Acacialaan 22, B-8400 Ostend, Belgium, 22 May 2014. Web. 29 May 2014. <a href="http://www.medcalc.org/calc/odds_ratio.php">http://www.medcalc.org/calc/odds_ratio.php</a></p>

			<h2>Details of LL:</h2>

			<p class="reference">Dunning, T. 1993. “Accurate methods for the statistics of surprise and coincidence”. Computational Lingusitics, 19 (1), 61–74.</p>
			<p class="reference">Rayson, P. &amp; Garside, R. 2000. “Comparing corpora using frequency profiling”. Proceedings of the Workshop on Comparing Corpora, held in conjunction with the 38th Annual Meeting of the Association for Computational Linguistics (ACL 2000), 1-8 October 2000, Hong Kong, 1–6. Available at: <a href="http://www.comp.lancs.ac.uk/~paul/publications/rg_acl2000.pdf">http://www.comp.lancs.ac.uk/~paul/publications/rg_acl2000.pdf</a></p>

			<h2>Details of OR:</h2>

			<p class="reference">Agresti, A. 2002. Categorical Data Analysis. 2nd edition. New York: Wiley.</p>
			<p class="reference">Agresti, A. 2007. An Introduction to Categorical Data Analysis. 2nd edition. New York: Wiley.</p>
			<p class="reference">Pagano M, Gauvreau K (2000) Principles of biostatistics. 2nd ed. Belmont, CA: Brooks/Cole.</p>
			<p class="reference">Deeks JJ, Higgins JPT (2010) Statistical algorithms in Review Manager 5. Retrieved from <a href="http://ims.cochrane.org/revman/documentation/Statistical-methods-in-RevMan-5.pdf">http://ims.cochrane.org/revman/documentation/Statistical-methods-in-RevMan-5.pdf</a></p>
		</section>

		<footer>
			<h1>Made by:</h1>
			<p>Programming: <a href="mailto:dougalg@gmail.com">Dougal Graham</a></p>
			<p>Consultation: <a href="mailto:irictodd@kmutt.ac.th">Richard Watson Todd</a>; <a href="mailto:punjaporn.poj@kmutt.ac.th">Punjaporn Pojanapunya</a></p>
		</footer>

	</div>
</template>

<style lang="scss" scoped>
.about-container {
	max-width: 630px;
}

h2 {
	font-size: 1.1em;
	margin: 1.2em 0 0.3em 0
}

h2+p {
	margin-top: 0
}

.reference {
	text-align: left;
	word-wrap: break-word;
	padding-left: 1em;
	text-indent: -1em
}

footer p {
	margin: 0
}
</style>

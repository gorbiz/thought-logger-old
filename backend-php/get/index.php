<?php
$entries = file('../../../thought.log', FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
$entries = array_map('json_decode', $entries);


echo '<?xml version="1.0" encoding="UTF-8" ?>' . PHP_EOL;
?><rss version="2.0">

	<channel>
		<title>Thought log</title>
		<description>This is a personal thought log</description>
		<link>http://localhost/thought_logger/get/</link>
		<lastBuildDate><?php echo date('r'); ?></lastBuildDate>
		<pubDate><?php echo date('r'); ?></pubDate>

		<?php foreach ($entries as $entry) : ?>
		<item>
			<title><?php echo $entry->content; ?></title>
			<description><?php echo $entry->content; ?></description>
			<link>http://www.exaample.com/</link>
			<pubDate><?php echo date('r', strtotime($entry->time)); ?></pubDate>
		</item>	
		<?php endforeach; ?>

	</channel>
</rss>
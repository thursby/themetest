<?php
/*
* Plugin Name: ThemeTest plugin
* Description: Do stuff for themetests
* Version: 0.1
* Author: Wayne Thursby
* Author URI: https://www.waynethursby.com
*/


function themetest_user_scripts() {
    $plugin_url = plugin_dir_url( __FILE__ );

    wp_enqueue_style( 'style',  $plugin_url . "/templates/rundown-template.css");
}

add_action( 'wp_enqueue_scripts', 'themetest_user_scripts' );

function themetest_results_full(){
?>

<p><?php the_field('theme_description'); ?></p>
<div class="themeinfo-container">
  <div class="top-container">
    <div class="screenshots-container">
      <figure>
        <a href="<?php the_field('theme_preview_url'); ?>" target="_blank">
        <img src="/theme-images/<?php the_field('theme_slug'); ?>.png" width="320" scale="0" /> 
        </a>
        <figcaption>Official Screenshot</figcaption>
      </figure>
      <br/> 
      <figure>
        <img src="/theme-images/<?php the_field('theme_slug'); ?>-ss.png" width="320" scale="0" />
        <figcaption>Fresh Install</figcaption>
      </figure>
    </div>
    <div class="themedata-container">
      <label class="themepage-label">Name</label>
      <div class="themepage-data"><?php the_field('theme_name'); ?></div>
      <label class="themepage-label">Version</label>
      <div class="themepage-data"><?php the_field('theme_version'); ?></div>
      <label class="themepage-label">Author</label>
      <div class="themepage-data"><?php the_field('theme_author'); ?></div>
      <label class="themepage-label">Rating</label>
      <div class="themepage-data"><?php the_field('theme_rating'); ?></div>
      <!-- TODO show stars-->
      <label class="themepage-label"># of Ratings</label>
      <div class="themepage-data"><?php the_field('theme_num_ratings'); ?></div>
      <label class="themepage-label">Downloads</label>
      <div class="themepage-data"><?php the_field('theme_downloaded'); ?></div>
      <label class="themepage-label">Last Update</label>
      <div class="themepage-data"><?php the_field('theme_last_updated'); ?></div>
      <label class="themepage-label">Homepage</label>
      <div class="themepage-data"><a href="<?php the_field('theme_homepage'); ?>"><?php the_field('theme_name'); ?></a></div>
    </div>
  </div>
</div>
<div class="top-stats">
  <div class="section-div">
    <div class="section-title">PageSpeed</div>
    <div class="second-row">
      <div class="score"><?php the_field('gt_pagespeed_score'); ?></div>
      <div class="lettergrade">A</div>
    </div>
  </div>
  <div class="section-div">
    <div class="section-title">YSlow</div>
    <div class="second-row">
      <div class="score"><?php the_field('gt_yslow_score'); ?></div>
      <div class="lettergrade">B</div>
    </div>
  </div>
  <div class="right-stats">
    <label class="themepage-label">Page Elements</label>
    <div class="themepage-data"><?php the_field('gt_page_elements'); ?></div>
    <label class="themepage-label">HTML Bytes</label>
    <div class="themepage-data"><?php the_field('gt_html_bytes'); ?></div>
    <label class="themepage-label">Page Bytes</label>
    <div class="themepage-data"><?php the_field('gt_page_bytes'); ?></div>
  </div>
</div>

<?php
}

add_shortcode('themetest_results_full', 'themetest_results_full');

/* Change Excerpt length */
function custom_excerpt_length( $length ) {
  return 1000;
}

add_filter('excerpt_length', 'custom_excerpt_length', 1000);

?>

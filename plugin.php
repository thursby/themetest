<?php
/*
* Plugin Name: ThemeTest plugin
* Description: Do stuff for themetests
* Version: 0.0.1 beta
* Author: Wayne Thursby
* Author URI: https://www.waynethursby.com
*/


function themetest_user_scripts() {
    $plugin_url = plugin_dir_url( __FILE__ );

    wp_enqueue_style( 'style',  $plugin_url . "/style.css");
}

add_action( 'wp_enqueue_scripts', 'themetest_user_scripts' );

function themetest_results_full(){
  $theme_name = get_field('theme_name', $post_id);
  $theme_version = get_field('theme_version', $post_id);
  $theme_featured_image = get_the_post_thumbnail_url($post_id);
  $theme_description = get_field('theme_description', $post_id);
  $theme_preview_url = get_field('theme_preview_url', $post_id);
  $theme_slug = get_field('theme_slug', $post_id);
  $theme_author = get_field('theme_author', $post_id);
  $theme_rating = get_field('theme_rating', $post_id);
  $theme_num_ratings = get_field('theme_num_ratings', $post_id);
  $theme_downloaded = get_field('theme_downloaded', $post_id);
  $theme_last_updated = get_field('theme_last_updated', $post_id);
  $theme_homepage = get_field('theme_homepage', $post_id);
  $theme_name = get_field('theme_name', $post_id);
  $gt_pagespeed_score = get_field('gt_pagespeed_score', $post_id);
  $gt_yslow_score = get_field('gt_yslow_score', $post_id);
  $gt_page_elements = get_field('gt_page_elements', $post_id);
  $gt_page_bytes = get_field('gt_page_bytes', $post_id);
  $gt_html_bytes = get_field('gt_html_bytes', $post_id);
  $gt_fully_loaded_time = get_field('gt_fully_loaded_time', $post_id);
  $gt_first_contentful_paint_time = get_field('gt_first_contentful_paint_time', $post_id);
  $gt_dom_content_loaded_duration = get_field('gt_dom_content_loaded_duration', $post_id);
  $gt_backend_duration = get_field('gt_backend_duration', $post_id);
  $gt_connect_duration = get_field('gt_connect_duration', $post_id);
  $gt_redirect_duration = get_field('gt_redirect_duration', $post_id);

  $res = <<<EOD
  <div class="container-fluid">

  <div class="row">
    <div class="col-sm-12">
      <p>$theme_description</p>
    </div>
  </div>
  <div class="row no-gutter">
    <div class="col-sm-6">
      <figure>
        <a href="$theme_preview_url" target="_blank">
        <img src="$theme_featured_image" width="320" scale="0"> 
        </a>
        <figcaption>Official Screenshot</figcaption>
      </figure>
    </div>
    <div class="col-sm-6">
      <figure>
        <img src="/theme-images/$theme_slug-ss.png" width="320" scale="0">
        <figcaption>Fresh Install</figcaption>
      </figure>
    </div>
  </div>
  <!--   end row -->
  <div class="row no-gutter data-row">
    <div class="col-sm-4 col-xs-12 no-gutter">
      <div class="col-xs-6 themepage-label">Name:</div>
      <div class="col-xs-6 themepage-data">$theme_name</div>
      <div class="col-xs-6 themepage-label">Version:</div>
      <div class="col-xs-6 themepage-data">$theme_version</div>
      <div class="col-xs-6 themepage-label">Author:</div>
      <div class="col-xs-6 themepage-data">$theme_author</div>
      <div class="col-xs-6 themepage-label">Rating:</div>
      <div class="col-xs-6 themepage-data">$theme_rating</div>
      <div class="col-xs-6 themepage-label"># of Ratings:</div>
      <div class="col-xs-6 themepage-data">$theme_num_ratings</div>
      <div class="col-xs-6 themepage-label">Downloads:</div>
      <div class="col-xs-6 themepage-data">$theme_downloaded</div>
      <div class="col-xs-6 themepage-label">Last Update:</div>
      <div class="col-xs-6 themepage-data">$theme_last_updated</div>
      <div class="col-xs-6 themepage-label">Homepage:</div>
      <div class="col-xs-6 themepage-data">
        <a href="$theme_homepage">
          $theme_name
        </a>
      </div>
    </div>
    <div class="col-sm-4 col-xs-12 no-gutter">
      <div class="row no-gutter">
        <div class="col-sm-12 col-xs-6 big_number_label">PageSpeed:</div>
        <div class="col-sm-12 col-xs-6 big_number">$gt_pagespeed_score</div>
      </div>
      <div class="row no-gutter">
        <div class="col-sm-12 col-xs-6 big_number_label">YSlow:</div>
        <div class="col-sm-12 col-xs-6 big_number">$gt_yslow_score</div>
      </div>
    </div>
    <div class="col-sm-4 col-xs-12 no-gutter">
      <div class="col-xs-6 themepage-label">Elements:</div>
      <div class="col-xs-6 themepage-data">$gt_page_elements</div>
      <div class="col-xs-6 themepage-label">Page Bytes:</div>
      <div class="col-xs-6 themepage-data">$gt_page_bytes B</div>
      <div class="col-xs-6 themepage-label">HTML Bytes:</div>
      <div class="col-xs-6 themepage-data">$gt_html_bytes B</div>
      <div class="col-xs-6 themepage-label">Load Time:</div>
      <div class="col-xs-6 themepage-data">$gt_fully_loaded_time ms</div>
      <div class="col-xs-6 themepage-label">FCP Time:</div>
      <div class="col-xs-6 themepage-data">$gt_first_contentful_paint_time ms</div>
      <div class="col-xs-6 themepage-label">DOM Int.:</div>
      <div class="col-xs-6 themepage-data">$gt_dom_content_loaded_duration ms</div>
      <div class="col-xs-6 themepage-label">Backend:</div>
      <div class="col-xs-6 themepage-data">$gt_backend_duration ms</div>
      <div class="col-xs-6 themepage-label">Connection:</div>
      <div class="col-xs-6 themepage-data">$gt_connect_duration ms</div>
      <div class="col-xs-6 themepage-label">Redirects:</div>
      <div class="col-xs-6 themepage-data">$gt_redirect_duration ms</div>
    </div>
  
  </div>
  <!--   end row -->
  </div>
  <!-- container -->
  
EOD;
  return $res;
}

function themetest_results_rundown($atts = [], $content = null, $tag = '') {
  $res = <<<EODA
<div class="container-fluid">
<div class="row">
  <div class="col-xs-12">
    <?php the_excerpt(); ?>
  </div>
</div>

EODA;

  foreach ($atts as $att) {
    $post_ids = explode(" ", $att);
  }
  foreach ($post_ids as $post_id) {
    $theme_name = get_field('theme_name', $post_id);
    $theme_featured_image = get_the_post_thumbnail_url($post_id);
    $theme_permalink = get_permalink($post_id);
    $theme_slug = get_field('theme_slug', $post_id);
    $theme_author = get_field('theme_author', $post_id);
    $theme_version = get_field('theme_version', $post_id);
    $theme_rating = get_field('theme_rating', $post_id);
    $theme_last_updated = get_field('theme_last_updated', $post_id);
    $theme_downloaded = get_field('theme_downloaded', $post_id);
    $gt_page_elements = get_field('gt_page_elements', $post_id);
    $gt_page_bytes = get_field('gt_page_bytes', $post_id);
    $gt_page_load_time = get_field('gt_page_load_time', $post_id);
    $gt_html_bytes = get_field('gt_html_bytes', $post_id);
    $gt_first_contentful_paint_time = get_field('gt_first_contentful_paint_time', $post_id);
    $gt_dom_interactive_time = get_field('gt_dom_interactive_time', $post_id);
    $gt_pagespeed_score = get_field('gt_pagespeed_score', $post_id);
    $gt_yslow_score = get_field('gt_yslow_score', $post_id);

    $newrow = <<<EODB
      <div class="row no-gutter">
        <div class="col-sm-3 col-xs-12">
        <a href="$theme_permalink" rel="noopener" target="_blank">
        <img src="$theme_featured_image" class="img-responsive img-rounded">
        </a>
        </div>
        <div class="col-sm-4 no-gutter">
          <div class="col-xs-4">
              <div class="themepage-label">Name:</div>
              <div class="themepage-label">Author:</div>
              <div class="themepage-label">Version:</div>
              <div class="themepage-label">Rating:</div>
              <div class="themepage-label hidden-md hidden-sm">Updated:</div>
              <div class="themepage-label hidden-md hidden-sm">DL Count:</div>
          </div>
          <div class="col-xs-8">
              <div class="themepage-data">$theme_name</div>
              <div class="themepage-data">$theme_author</div>
              <div class="themepage-data">$theme_version</div>
              <div class="themepage-data">$theme_rating</div>
              <div class="themepage-data hidden-md hidden-sm">$theme_last_updated</div>
              <div class="themepage-data hidden-md hidden-sm">$theme_downloaded</div>
          </div>
        </div>
        <div class="col-sm-4 no-gutter">
          <div class="col-sm-7 col-xs-4">
              <div class="themepage-label">Elements:</div>
              <div class="themepage-label">Page Bytes:</div>
              <div class="themepage-label">Load Time:</div>
              <div class="themepage-label hidden-md hidden-sm">HTML Bytes:</div>
              <div class="themepage-label hidden-md hidden-sm">FCP Time:</div>
              <div class="themepage-label hidden-md hidden-sm">DOM Int.:</div>
          </div>
          <div class="col-sm-5 col-xs-8">
              <div class="themepage-data">$gt_page_elements</div>
              <div class="themepage-data">$gt_page_bytes B</div>
              <div class="themepage-data">$gt_page_load_time ms</div>
              <div class="themepage-data hidden-md hidden-sm">$gt_html_bytes B</div>
              <div class="themepage-data hidden-md hidden-sm">$gt_first_contentful_paint_time ms</div>
              <div class="themepage-data hidden-md hidden-sm">$gt_dom_interactive_time ms</div>
          </div>
        </div>
        
        <div class="col-sm-1 no-gutter">
          <div class="row no-gutter">
          <div class="col-sm-12 col-xs-4 big_number_label">PageSpeed<div class="visible-xs visible-xs-inline-block">:</div></div>
          <div class="col-sm-12 col-xs-8 big_number">$gt_pagespeed_score</div>
          </div>
          <div class="row no-gutter">
          <div class="col-sm-12 col-xs-4 big_number_label">YSlow<div class="visible-xs visible-xs-inline-block">:</div></div>
          <div class="col-sm-12 col-xs-8 big_number">$gt_yslow_score</div>
          </div>
        </div>
    
      </div> <!-- row -->
EODB;

    $res .= $newrow;
  }
  $res .= "</div> <!-- container -->";
  return $res;
}

add_shortcode('themetest_results_full', 'themetest_results_full');
add_shortcode('themetest_results_rundown', 'themetest_results_rundown');

/* Change Excerpt length */
function custom_excerpt_length( $length ) {
  return 1000;
}

add_filter('excerpt_length', 'custom_excerpt_length', 1000);

?>

---
layout: default
permalink: /vcsel_paper/
title: Redirecting
---

<h1>Preprint coming soon</h1>
<p>This QR code will redirect to the arXiv paper once it is posted.</p>

<p id="fallback"></p>

<script>
  // Only change this line when your paper is live.
  const target = "https://arxiv.org/abs/2604.17678";

  // If you've set a real URL, redirect.
  if (!target.includes("XXXX")) {
    window.location.replace(target);
  }

  // Set fallback link.
  if (!target.includes("XXXX")) {
    document.getElementById("fallback").innerHTML =
      'If you are not redirected, <a href="' + target + '">click here</a>.';
  }
</script>

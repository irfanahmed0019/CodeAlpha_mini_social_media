// ---- Like AJAX ----
document.addEventListener('DOMContentLoaded', function() {

  function getCsrfToken() {
    return document.cookie.split(';')
      .map(c => c.trim())
      .find(c => c.startsWith('csrftoken='))
      ?.split('=')[1] || '';
  }

  // Like buttons
  document.querySelectorAll('.like-btn').forEach(function(btn) {
    btn.addEventListener('click', function() {
      const postId = this.dataset.postId;
      const countEl = this.querySelector('.like-count');
      const icon = this.querySelector('.like-icon');

      fetch('/ajax/like/' + postId + '/', {
        method: 'POST',
        headers: {
          'X-CSRFToken': getCsrfToken(),
          'Content-Type': 'application/json',
        },
      })
      .then(r => r.json())
      .then(data => {
        if (data.liked) {
          this.classList.add('liked');
          icon.textContent = 'favorite';
          icon.style.fontVariationSettings = "'FILL' 1";
        } else {
          this.classList.remove('liked');
          icon.textContent = 'favorite';
          icon.style.fontVariationSettings = "'FILL' 0";
        }
        if (countEl) countEl.textContent = data.count;
        icon.classList.add('heart-pop');
        icon.addEventListener('animationend', () => icon.classList.remove('heart-pop'), { once: true });
      })
      .catch(err => console.error(err));
    });
  });

  // Follow buttons
  document.querySelectorAll('.follow-btn').forEach(function(btn) {
    btn.addEventListener('click', function() {
      const username = this.dataset.username;
      const followersCount = document.querySelector('.followers-count');

      fetch('/ajax/follow/' + username + '/', {
        method: 'POST',
        headers: { 'X-CSRFToken': getCsrfToken() },
      })
      .then(r => r.json())
      .then(data => {
        if (data.following) {
          this.textContent = 'Following';
          this.classList.remove('not-following');
          this.classList.add('is-following');
        } else {
          this.textContent = 'Follow';
          this.classList.remove('is-following');
          this.classList.add('not-following');
        }
        if (followersCount) followersCount.textContent = data.followers_count;
      })
      .catch(err => console.error(err));
    });
  });

  // Button press micro-interaction
  document.querySelectorAll('button, .btn-primary, .btn-secondary').forEach(function(btn) {
    btn.addEventListener('mousedown', function() {
      this.style.transition = 'transform 0.07s, box-shadow 0.07s';
    });
  });

  // Auto-growing textarea
  document.querySelectorAll('textarea').forEach(function(ta) {
    ta.addEventListener('input', function() {
      this.style.height = 'auto';
      this.style.height = (this.scrollHeight) + 'px';
    });
  });

  // Character counter for post textarea
  const postTextarea = document.querySelector('#id_content');
  const charCounter = document.querySelector('#char-counter');
  if (postTextarea && charCounter) {
    postTextarea.addEventListener('input', function() {
      const remaining = 2200 - this.value.length;
      charCounter.textContent = remaining;
      charCounter.style.color = remaining < 100 ? '#bb010d' : '#8a6555';
    });
  }

  // Search live suggestions
  const searchInput = document.querySelector('#search-input');
  const searchResults = document.querySelector('#search-results');
  let searchTimeout;
  if (searchInput && searchResults) {
    searchInput.addEventListener('input', function() {
      clearTimeout(searchTimeout);
      const q = this.value.trim();
      if (q.length < 2) { searchResults.innerHTML = ''; searchResults.style.display = 'none'; return; }
      searchTimeout = setTimeout(() => {
        fetch('/ajax/search/?q=' + encodeURIComponent(q))
          .then(r => r.json())
          .then(data => {
            if (data.users.length === 0) { searchResults.style.display = 'none'; return; }
            searchResults.innerHTML = data.users.map(u =>
              `<a href="${u.url}" class="search-result-item">
                <span class="avatar avatar-sm" style="background:#ffeadf">${u.username[0].toUpperCase()}</span>
                <span>${u.display_name} <small style="color:#8a6555">@${u.username}</small></span>
              </a>`
            ).join('');
            searchResults.style.display = 'block';
          });
      }, 250);
    });
    document.addEventListener('click', e => {
      if (!searchInput.contains(e.target)) { searchResults.style.display = 'none'; }
    });
  }

  // Image preview before upload
  const imageInput = document.querySelector('#id_image');
  const imagePreview = document.querySelector('#image-preview');
  if (imageInput && imagePreview) {
    imageInput.addEventListener('change', function() {
      const file = this.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = e => {
          imagePreview.src = e.target.result;
          imagePreview.style.display = 'block';
        };
        reader.readAsDataURL(file);
      }
    });
  }

  // Fade in post cards
  document.querySelectorAll('.post-card, .fade-in').forEach((el, i) => {
    el.style.opacity = 0;
    el.style.transform = 'translateY(8px)';
    setTimeout(() => {
      el.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
      el.style.opacity = 1;
      el.style.transform = 'translateY(0)';
    }, i * 60);
  });

});

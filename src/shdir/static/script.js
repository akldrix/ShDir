document.getElementById('search-input').addEventListener('input', function (e) {
        const query = e.target.value.toLowerCase().trim();
        const items = document.querySelectorAll('.search-item');

        items.forEach(function (item) {
          const itemName = item.getAttribute('data-name');

          if (itemName.includes(query)) {
            item.classList.remove('hidden');
          } else {
            item.classList.add('hidden');
          }
        });
      });


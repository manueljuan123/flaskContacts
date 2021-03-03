const btnDelete = document.querySelectorAll('.btn-delete')

if(btnDelete){
    const btnArray = Array.from(btnDelete);
    btnArray.forEach((btn) => {
        btn.addEventListener('click', function (e) {
                if (!confirm('Do you want to delete it?')) {
                    e.preventDefault();
                }
            });
    });
}

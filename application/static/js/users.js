let inputSearch;
let tableRows;


function searchUser() {
    let searchQuery = inputSearch.value.toUpperCase();
    for (let i = 0, length = tableRows.length; i < length; i++) {
        row = tableRows[i];
        let tableCell = row.getElementsByTagName('td')[1];
        if (tableCell) {
            let txtValue = tableCell.textContent || tableCell.innerText;
            if (txtValue.toUpperCase().includes(searchQuery)) {
                row.style.display = "";
            } else {
                row.style.display = 'none';
            }
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    inputSearch = document.getElementById('userSearch');
    let userTable = document.getElementById('userTable');
    tableRows = userTable.getElementsByTagName('tr');

    inputSearch.addEventListener('keyup', searchUser);
});
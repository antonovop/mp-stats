function toggle_visibility(first_id, second_id, mode) {
    const first_item = document.getElementById(first_id)
    const second_item = document.getElementById(second_id)

    if (mode == 'first') {
        first_item.style.display = 'block'
        second_item.style.display = 'none'
        return
    }
    if (mode == 'second') {
        first_item.style.display = 'none'
        second_item.style.display = 'block'
        return
    }
    first_item.style.display = 'none'
    second_item.style.display = 'none'
}
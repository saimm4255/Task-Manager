const tasks = document.querySelectorAll('.task');
tasks.forEach(task => {
    task.addEventListener('dragstart', () => {
        task.classList.add('dragging');
    });
    task.addEventListener('dragend', () => {
        task.classList.remove('dragging');
    });
});

export const useUI = () => {
  const isDarkMode = useState<boolean>('darkMode', () => false);
  const sidebarOpen = useState<boolean>('sidebarOpen', () => false);
  
  // Carregar preferência de tema do localStorage
  onMounted(() => {
    if (process.client) {
      const savedMode = localStorage.getItem('darkMode');
      if (savedMode) {
        isDarkMode.value = savedMode === 'true';
        applyTheme();
      }
    }
  });
  
  const toggleDarkMode = () => {
    isDarkMode.value = !isDarkMode.value;
    if (process.client) {
      localStorage.setItem('darkMode', isDarkMode.value.toString());
      applyTheme();
    }
  };
  
  const applyTheme = () => {
    if (process.client) {
      if (isDarkMode.value) {
        document.documentElement.classList.add('dark');
      } else {
        document.documentElement.classList.remove('dark');
      }
    }
  };
  
  const toggleSidebar = () => {
    sidebarOpen.value = !sidebarOpen.value;
  };
  
  const closeSidebar = () => {
    sidebarOpen.value = false;
  };
  
  return {
    isDarkMode,
    toggleDarkMode,
    sidebarOpen,
    toggleSidebar,
    closeSidebar
  };
};

var elementsDown2 = document.getElementsByClassName("dropdown-content2");
var value = "";
var valuename = "";
var globalfileExtension = "";
var same = false;
var selectedFiles = [];
var sessionId = generateSessionId();

// Clipboard functionality
var clipboardEnabled = false;

var elementsPandoc = document.getElementsByClassName("pandoc");
var elementsExel = document.getElementsByClassName("exel");
var elementsPPT = document.getElementsByClassName("ppt");
var elementsVideo = document.getElementsByClassName("video");
var elementsAudio = document.getElementsByClassName("audio");
var elementsImage = document.getElementsByClassName("image");

var videoGruppe = [];
var audioGruppe = [];
var imageGruppe = [];
var tabelleGruppe = [];
var persentGruppe = [];
var pandocGruppe = [];
var convertFile = [];

function generateSessionId() {
  return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
}

document.getElementById('sessionId').value = sessionId;

fetch("/static/data/formats.json")
  .then(res => {
    if (!res.ok) throw new Error("Fehler beim Laden der JSON-Datei");
    return res.json();
  })
  .then(data => {
    const addDot = arr => arr.map(ext => '.' + ext);

    videoGruppe = addDot(data.videoGruppe);
    audioGruppe = addDot(data.audioGruppe);
    imageGruppe = addDot(data.imageGruppe);
    tabelleGruppe = addDot(data.tabelleGruppe);
    persentGruppe = addDot(data.persentGruppe);
    pandocGruppe = addDot(data.pandocGruppe);
    convertFile = addDot(data.convertFile);

    console.log("Formats loaded successfully");
  })
  .catch(err => console.error(err));

// Clipboard Event Listeners
document.addEventListener('DOMContentLoaded', function() {
  // Enable clipboard when page loads
  clipboardEnabled = true;
  
  // Show clipboard info
  showClipboardInfo();
});

// Clipboard paste event
document.addEventListener('paste', function(e) {
  if (!clipboardEnabled) return;
  
  const items = e.clipboardData.items;
  let newFiles = [];
  
  for (let i = 0; i < items.length; i++) {
    const item = items[i];
    
    if (item.type.indexOf('image/') === 0) {
      // Handle pasted images
      const file = item.getAsFile();
      if (file) {
        // Generate a filename for pasted images
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
        const extension = file.type.split('/')[1] || '';
        const filename = `pasted-image-${timestamp}.${extension}`;
        
        // Create new file with proper name
        const renamedFile = new File([file], filename, { type: file.type });
        newFiles.push(renamedFile);
      }
    } else if (item.kind === 'file') {
      // Handle other file types
      const file = item.getAsFile();
      if (file) {
        newFiles.push(file);
      }
    }
  }
  
  if (newFiles.length > 0) {
    addFilesToSelection(newFiles);
    e.preventDefault();
    showClipboardSuccess(newFiles.length);
  }
});

// Keyboard shortcut (Ctrl+V)
document.addEventListener('keydown', function(e) {
  if ((e.ctrlKey || e.metaKey) && e.key === 'v' && clipboardEnabled) {
    // Paste event will be triggered automatically
    console.log('Paste shortcut detected');
  }
});

function addFilesToSelection(newFiles) {
  // Add new files to existing selection
  newFiles.forEach(file => {
    selectedFiles.push(file);
  });
  
  // Update file input with combined files
  const dt = new DataTransfer();
  selectedFiles.forEach(file => {
    dt.items.add(file);
  });
  fileInput.files = dt.files;
  
  // Update display
  handleFileSelection();
}


function showClipboardSuccess(fileCount) {
  const existingNotification = document.getElementById('clipboardNotification');
  if (existingNotification) {
    existingNotification.remove();
  }
  
  const notification = document.createElement('div');
  notification.id = 'clipboardNotification';
  notification.className = 'clipboard-notification success';
  notification.innerHTML = `
    <div class="notification-icon">✅</div>
    <span>${fileCount} file${fileCount > 1 ? 's' : ''} pasted from clipboard!</span>
  `;
  
  document.body.appendChild(notification);
  
  // Show notification
  setTimeout(() => {
    notification.classList.add('show');
  }, 100);
  
  // Hide notification after 3 seconds
  setTimeout(() => {
    notification.classList.remove('show');
    setTimeout(() => {
      if (notification.parentNode) {
        notification.remove();
      }
    }, 300);
  }, 3000);
}

const dropOverlay = document.getElementById('dropOverlay');
const fileInput = document.getElementById('fileInput');
let dragCounter = 0;

// Drag and Drop functions
function showOverlay() {
  dropOverlay.style.display = 'flex';
}

function hideOverlay() {
  dropOverlay.style.display = 'none';
}

document.body.addEventListener('dragenter', (e) => {
  if (e.dataTransfer && e.dataTransfer.items && e.dataTransfer.items.length > 0) {
    dragCounter++;
    showOverlay();
    dropOverlay.classList.add('highlight');
  }
});

document.body.addEventListener('dragleave', (e) => {
  dragCounter--;
  if (dragCounter <= 0) {
    dropOverlay.classList.remove('highlight');
    hideOverlay();
    dragCounter = 0;
  }
});

document.body.addEventListener('dragover', (e) => {
  e.preventDefault();
});

dropOverlay.addEventListener('drop', (e) => {
  e.preventDefault();
  hideOverlay();
  dropOverlay.classList.remove('highlight');
  dragCounter = 0;
  
  const files = e.dataTransfer.files;
  if (files && files.length > 0) {
    const dt = new DataTransfer();
    for (let i = 0; i < files.length; i++) {
      dt.items.add(files[i]);
    }
    fileInput.files = dt.files;
    handleFileSelection();
    e.dataTransfer.clearData();
  }
});

function filterFunction(dropdownClass) {
  const input = document.querySelector(`.${dropdownClass} .suche`);
  const filter = input.value.toLowerCase();
  const pElements = document.querySelectorAll(`.${dropdownClass} p`);

  pElements.forEach(function (item) {
    item.style.display = "flex";
  });

  pElements.forEach(function (item) {
    const textValue = item.textContent.toLowerCase(); 
    if (textValue.indexOf(filter) == -1) {
      item.style.display = "none";
    } else {
      item.style.display = "flex";
    }
  });

  if (elementsDown2.length > 0 && window.getComputedStyle(elementsDown2[0]).display === "flex" && input.value.trim() === "") {
    console.log(globalfileExtension)
    meineFunktion(globalfileExtension);
  }
}

function setFileFunction(name, filename) {
  value = name;
  valuename = filename;
  console.log(value, valuename);

  if (elementsDown2.length > 0 && window.getComputedStyle(elementsDown2[0]).display === "flex") {
    var dropbtn2 = document.getElementsByClassName("dropbtn2");
    if (dropbtn2.length > 0) {
      dropbtn2[0].innerHTML = valuename;
    }
  }
  overfeed();
  return [value, valuename];
}

function handleFileSelection() {
  const fileInput = document.getElementById('fileInput');
  const fileLabel = document.getElementById('fileLabel');
  
  if (fileInput.files.length > 0) {
    selectedFiles = Array.from(fileInput.files);
    
    // Update label text
    if (selectedFiles.length === 1) {
      fileLabel.textContent = selectedFiles[0].name;
    } else {
      fileLabel.textContent = `${selectedFiles.length} files selected`;
    }
    
    // Validate all files and get extensions
    let allValid = true;
    let extensions = new Set();
    let firstValidExtension = "";
    
    selectedFiles.forEach(file => {
      const fileName = file.name;
      const fileExtension = '.' + fileName.split('.').pop().toLowerCase();
      extensions.add(fileExtension);
      
      if (!convertFile.includes(fileExtension)) {
        allValid = false;
      } else if (firstValidExtension === "") {
        firstValidExtension = fileExtension;
      }
    });
    
    if (!allValid) {
      errorMessage("Invalidfile");
      return;
    }
    
    // Check if all files have the same extension (same group compatibility)
    if (extensions.size > 1) {
      // Multiple different extensions - check if they're all in the same conversion group
      let groups = [videoGruppe, audioGruppe, imageGruppe, tabelleGruppe, persentGruppe, pandocGruppe];
      let fileGroups = new Set();
      
      extensions.forEach(ext => {
        let group = groups.findIndex(g => g.includes(ext));
        if (group !== -1) {
          fileGroups.add(group);
        }
      });
      
      if (fileGroups.size > 1) {
        errorMessage("mixedtypes");
        return;
      }
    }
    
    // Use first extension for group detection
    globalfileExtension = firstValidExtension;
    
    // Show file list
    updateFileList();
    overfeed();
    flexElemente();
    meineFunktion(globalfileExtension);
    errorMessage("none");
  } else {
    fileLabel.textContent = 'Select Files';
    document.getElementById('fileListContainer').style.display = 'none';
    errorMessage("none");
  }
}

function updateFileList() {
  const fileListContainer = document.getElementById('fileListContainer');
  const fileList = document.getElementById('fileList');
  
  if (selectedFiles.length === 0) {
    fileListContainer.style.display = 'none';
    return;
  }
  
  fileListContainer.style.display = 'block';
  fileList.innerHTML = '';
  
  selectedFiles.forEach((file, index) => {
    const fileItem = document.createElement('div');
    fileItem.className = 'file-item';
    
    fileItem.innerHTML = `
      <span class="file-name">${file.name}</span>
      <button class="delete-btn" onclick="removeFile(${index})" title="Remove file">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M3 6h18"></path>
          <path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"></path>
          <path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"></path>
          <line x1="10" y1="11" x2="10" y2="17"></line>
          <line x1="14" y1="11" x2="14" y2="17"></line>
        </svg>
      </button>
    `;
    
    fileList.appendChild(fileItem);
  });
}

function removeFile(index) {
  selectedFiles.splice(index, 1);
  
  // Update file input
  const dt = new DataTransfer();
  selectedFiles.forEach(file => {
    dt.items.add(file);
  });
  fileInput.files = dt.files;
  
  // Update display
  const fileLabel = document.getElementById('fileLabel');
  if (selectedFiles.length === 0) {
    fileLabel.textContent = 'Select Files';
    document.getElementById('fileListContainer').style.display = 'none';
  } else if (selectedFiles.length === 1) {
    fileLabel.textContent = selectedFiles[0].name;
  } else {
    fileLabel.textContent = `${selectedFiles.length} files selected`;
  }
  
  updateFileList();
  overfeed();
}

document.getElementById('fileInput').addEventListener('change', handleFileSelection);

function flexElemente() {
  function setDisplayFlex(elements) {
    for (var i = 0; i < elements.length; i++) {
      elements[i].style.display = "flex";
    }
  }

  setDisplayFlex(elementsExel);
  setDisplayFlex(elementsPPT);
  setDisplayFlex(elementsVideo);
  setDisplayFlex(elementsAudio);
  setDisplayFlex(elementsImage);
  setDisplayFlex(elementsPandoc);
}

function meineFunktion(name) {
  if (pandocGruppe.includes(name)) {
    for (var i = 0; i < elementsExel.length; i++) {
      elementsExel[i].style.display = "none";
    }
    for (var i = 0; i < elementsPPT.length; i++) {
      elementsPPT[i].style.display = "none";
    }
    for (var i = 0; i < elementsVideo.length; i++) {
      elementsVideo[i].style.display = "none";
    }
    for (var i = 0; i < elementsAudio.length; i++) {
      elementsAudio[i].style.display = "none";
    }
    for (var i = 0; i < elementsImage.length; i++) {
      elementsImage[i].style.display = "none";
    }
  } else if (tabelleGruppe.includes(name)) {
    for (var i = 0; i < elementsPPT.length; i++) {
      elementsPPT[i].style.display = "none";
    }
    for (var i = 0; i < elementsPandoc.length; i++) {
      elementsPandoc[i].style.display = "none";
    }
    for (var i = 0; i < elementsVideo.length; i++) {
      elementsVideo[i].style.display = "none";
    }
    for (var i = 0; i < elementsAudio.length; i++) {
      elementsAudio[i].style.display = "none";
    }
    for (var i = 0; i < elementsImage.length; i++) {
      elementsImage[i].style.display = "none";
    }
  } else if (persentGruppe.includes(name)) {
    for (var i = 0; i < elementsPandoc.length; i++) {
      elementsPandoc[i].style.display = "none";
    }
    for (var i = 0; i < elementsExel.length; i++) {
      elementsExel[i].style.display = "none";
    }
    for (var i = 0; i < elementsVideo.length; i++) {
      elementsVideo[i].style.display = "none";
    }
    for (var i = 0; i < elementsAudio.length; i++) {
      elementsAudio[i].style.display = "none";
    }
    for (var i = 0; i < elementsImage.length; i++) {
      elementsImage[i].style.display = "none";
    }
  } else if (videoGruppe.includes(name)) {
    for (var i = 0; i < elementsPandoc.length; i++) {
      elementsPandoc[i].style.display = "none";
    }
    for (var i = 0; i < elementsExel.length; i++) {
      elementsExel[i].style.display = "none";
    }
    for (var i = 0; i < elementsPPT.length; i++) {
      elementsPPT[i].style.display = "none";
    }
    for (var i = 0; i < elementsImage.length; i++) {
      elementsImage[i].style.display = "none";
    }
  } else if (audioGruppe.includes(name)) {
    for (var i = 0; i < elementsPandoc.length; i++) {
      elementsPandoc[i].style.display = "none";
    }
    for (var i = 0; i < elementsExel.length; i++) {
      elementsExel[i].style.display = "none";
    }
    for (var i = 0; i < elementsPPT.length; i++) {
      elementsPPT[i].style.display = "none";
    }
    for (var i = 0; i < elementsVideo.length; i++) {
      elementsVideo[i].style.display = "none";
    }
    for (var i = 0; i < elementsImage.length; i++) {
      elementsImage[i].style.display = "none";
    }
  } else if (imageGruppe.includes(name)) {
    for (var i = 0; i < elementsPandoc.length; i++) {
      elementsPandoc[i].style.display = "none";
    }
    for (var i = 0; i < elementsExel.length; i++) {
      elementsExel[i].style.display = "none";
    }
    for (var i = 0; i < elementsPPT.length; i++) {
      elementsPPT[i].style.display = "none";
    }
    for (var i = 0; i < elementsVideo.length; i++) {
      elementsVideo[i].style.display = "none";
    }
    for (var i = 0; i < elementsAudio.length; i++) {
      elementsAudio[i].style.display = "none";
    }
  }
}

function sendData() {
  if (same == true && selectedFiles.length > 0) {
    fetch('/empfange_daten', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ daten: valuename })
    })
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok.');
        }
        return response.json();
      })
      .then(data => {
        console.log('Success:', data);
        document.getElementById('uploadForm').submit();
      })
      .catch((error) => {
        console.error('Error:', error);
      });
  } else if (selectedFiles.length === 0) {
    errorMessage("nofiles");
  } else {
    errorMessage("nottype");
  }
}

document.querySelectorAll('.dropdown2').forEach(dropdown => {
  dropdown.addEventListener('mouseenter', () => {
    const dropdownContent = dropdown.querySelector('.dropdown-content2');
    dropdownContent.style.maxHeight = '300px';
    dropdownContent.style.opacity = '1';
  });

  dropdown.addEventListener('mouseleave', () => {
    const dropdownContent = dropdown.querySelector('.dropdown-content2');
    dropdownContent.style.maxHeight = '0';
    dropdownContent.style.opacity = '0';
  });
});

function updateFileName() {
  // This function is now replaced by handleFileSelection
  // Kept for compatibility
  handleFileSelection();
}

function errorMessage(element) {
  const errorElement = document.getElementById('error');

  if (element == "Invalidfile") {
    errorElement.innerHTML = 'Invalid file format. More details: <a href="/docs" target="_blank">Docs</a>';
  } else if (element == "notsame") {
    errorElement.innerHTML = 'Cannot be converted to the selected format.';
  } else if (element == "nottype") {
    errorElement.innerHTML = 'No target format selected';
  } else if (element == "nofiles") {
    errorElement.innerHTML = 'No files selected';
  } else if (element == "mixedtypes") {
    errorElement.innerHTML = 'All files must be of the same type (e.g., all images, all documents, etc.)';
  } else if (element == "none") {
    errorElement.innerHTML = '';
  }
}

function overfeed() {
  if (valuename !== "" && selectedFiles.length > 0) {
    let groups = [videoGruppe, audioGruppe, imageGruppe, tabelleGruppe, persentGruppe, pandocGruppe];
    let targetFormat = "." + valuename;
    let allCompatible = true;
    
    // Check if all selected files are compatible with the target format
    selectedFiles.forEach(file => {
      const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
      
      let sourceGroup = groups.find(group => group.includes(fileExtension));
      let targetGroup = groups.find(group => group.includes(targetFormat));
      
      if (!sourceGroup || !targetGroup || sourceGroup !== targetGroup) {
        allCompatible = false;
      }
    });
    
    // Also check if all files are in the same group (no mixing different types)
    if (allCompatible && selectedFiles.length > 1) {
      let fileGroups = new Set();
      selectedFiles.forEach(file => {
        const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
        let groupIndex = groups.findIndex(group => group.includes(fileExtension));
        if (groupIndex !== -1) {
          fileGroups.add(groupIndex);
        }
      });
      
      if (fileGroups.size > 1) {
        allCompatible = false;
      }
    }
    
    if (allCompatible) {
      console.log("All files are compatible with target format");
      errorMessage("none");
      same = true;
    } else {
      console.log("Some files are not compatible with target format or files are of different types");
      if (selectedFiles.length > 1) {
        // Check if it's a mixed types issue
        let groups = [videoGruppe, audioGruppe, imageGruppe, tabelleGruppe, persentGruppe, pandocGruppe];
        let fileGroups = new Set();
        selectedFiles.forEach(file => {
          const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
          let groupIndex = groups.findIndex(group => group.includes(fileExtension));
          if (groupIndex !== -1) {
            fileGroups.add(groupIndex);
          }
        });
        
        if (fileGroups.size > 1) {
          errorMessage("mixedtypes");
        } else {
          errorMessage("notsame");
        }
      } else {
        errorMessage("notsame");
      }
      same = false;
    }
  } else {
    same = false;
  }
}
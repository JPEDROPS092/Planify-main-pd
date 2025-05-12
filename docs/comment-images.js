const fs = require('fs');
const path = require('path');

// Function to recursively find all markdown files in a directory
function findMarkdownFiles(dir, fileList = []) {
  const files = fs.readdirSync(dir);
  
  files.forEach(file => {
    const filePath = path.join(dir, file);
    const stat = fs.statSync(filePath);
    
    if (stat.isDirectory()) {
      findMarkdownFiles(filePath, fileList);
    } else if (file.endsWith('.md')) {
      fileList.push(filePath);
    }
  });
  
  return fileList;
}

// Function to comment out image references in a markdown file
function commentOutImageReferences(filePath) {
  console.log(`Processing ${filePath}...`);
  
  let content = fs.readFileSync(filePath, 'utf8');
  
  // Replace image references with commented versions
  const modifiedContent = content.replace(/!\[.*?\]\(\/img\/docs\/.*?\.png\)/g, 
    match => `<!-- ${match} -->`);
  
  if (content !== modifiedContent) {
    fs.writeFileSync(filePath, modifiedContent, 'utf8');
    console.log(`Modified ${filePath}`);
    return true;
  }
  
  return false;
}

// Main function
function main() {
  const docsDir = path.join(__dirname, 'docs');
  const markdownFiles = findMarkdownFiles(docsDir);
  
  console.log(`Found ${markdownFiles.length} markdown files.`);
  
  let modifiedCount = 0;
  
  markdownFiles.forEach(file => {
    if (commentOutImageReferences(file)) {
      modifiedCount++;
    }
  });
  
  console.log(`\nDone! Modified ${modifiedCount} files.`);
}

main();

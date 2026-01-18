#!/usr/bin/env node
/**
 * Generate a secure API key for Vector Storage Service
 * Usage: node generate-api-key.js
 */

const crypto = require('crypto');
const fs = require('fs');
const path = require('path');
const readline = require('readline');

function generateApiKey(length = 32) {
  return crypto.randomBytes(length).toString('hex');
}

function createEnvFile(apiKey) {
  const envContent = `# Vector Storage Service Configuration
# Generated: ${new Date().toISOString()}

# Security - IMPORTANT!
API_KEY=${apiKey}

# CORS (Optional - comma separated origins)
# ALLOWED_ORIGINS=https://your-express-app.com,https://your-frontend.com

# Server Configuration (Optional)
# PORT=8000
# HOST=0.0.0.0
`;

  fs.writeFileSync('.env', envContent);
  console.log('✅ .env file created successfully!');
  console.log(`📁 Location: ${path.resolve('.env')}`);
}

async function promptUser(question) {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });

  return new Promise((resolve) => {
    rl.question(question, (answer) => {
      rl.close();
      resolve(answer);
    });
  });
}

async function main() {
  console.log('🔐 Vector Storage Service - API Key Generator');
  console.log('='.repeat(50));

  // Check if .env already exists
  if (fs.existsSync('.env')) {
    const response = await promptUser('\n⚠️  .env file already exists. Overwrite? (y/N): ');
    if (response.toLowerCase() !== 'y') {
      console.log('❌ Cancelled. Existing .env file kept.');
      return;
    }
  }

  // Generate API key
  console.log('\n🔑 Generating secure API key...');
  const apiKey = generateApiKey();

  // Create .env file
  createEnvFile(apiKey);

  console.log('\n' + '='.repeat(50));
  console.log('🎉 Setup Complete!');
  console.log('='.repeat(50));
  console.log('\n📋 Your API Key:');
  console.log(`   ${apiKey}`);
  console.log('\n⚠️  Keep this key secret! Don\'t commit to Git.');
  console.log('\n📝 Next steps:');
  console.log('   1. Add .env to .gitignore (if not already)');
  console.log('   2. Set API_KEY on Railway/Cloud Run deployment');
  console.log('   3. Add API key to your Express server .env:');
  console.log(`      VECTOR_STORAGE_API_KEY=${apiKey}`);
  console.log('\n🚀 Ready to deploy!');
  console.log('\n📖 See INTEGRATION-GUIDE.md for usage examples');
}

main().catch(console.error);

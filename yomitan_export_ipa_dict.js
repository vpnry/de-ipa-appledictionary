const fs = require('fs');
const readline = require('readline');
const { Dictionary, DictionaryIndex, TermEntry } = require('yomichan-dict-builder');

async function buildDict() {
  const csvFilePath = './de_word_ipa.csv';
  const outputZip = 'yomitan_de_ipa.zip';

  const dictionary = new Dictionary({
    fileName: outputZip,
  });

  const index = new DictionaryIndex()
    .setTitle('German IPA Dictionary')
    .setRevision('1.0')
    .setAuthor('Vpnry')
    .setAttribution('German IPA data (CC0: Public Domain) is from https://www.kaggle.com/datasets/cdminix/german-ipa-pronunciation-dictionary')
    .setUrl('https://github.com/vpnry/de-ipa-appledictionary')
    .setDescription('IPA readings for German words from de_word_ipa.csv')
    .build();

  await dictionary.setIndex(index);

  const fileStream = fs.createReadStream(csvFilePath);
  const rl = readline.createInterface({
    input: fileStream,
    crlfDelay: Infinity
  });

  let lineCount = 0;
  for await (const line of rl) {
    lineCount++;
    if (lineCount === 1) continue; // Skip header

    const parts = line.split(',');
    if (parts.length < 2) continue;

    const word = parts[0];
    const ipa = parts[1];

    if (!word || !ipa) continue;

    const entry = new TermEntry(word)
      .setReading(word)
      .addDetailedDefinition({
        type: 'structured-content',
        content: [
          {
            tag: 'span',
            content: `IPA: | ${ipa} |`
          }
        ]
      })
      .build();

    await dictionary.addTerm(entry);

    if (lineCount % 10000 === 0) {
      console.log(`Processed ${lineCount} lines...`);
    }
  }

  console.log('Exporting dictionary...');
  const stats = await dictionary.export('./');
  console.log('Done!');
  console.table(stats);
}

buildDict().catch(console.error);

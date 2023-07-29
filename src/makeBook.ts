import * as fs from "fs";
import { Document, Packer, Paragraph, TextRun } from "docx";
const HTMLtoDOCX = require('html-to-docx');

// Documents contain sections, you can have multiple sections per document, go here to learn more about sections
// This simple example will only contain one section
const sampleText = "If you have any questions or comments about the philosophy and practice of the teachings of Sri Ramana, or about any of my writings, whether those contained in my book, <a href=\"http://www.happinessofbeing.com/resources/happiness_art_being.html\" target=\"_blank\"><i>Happiness and the Art of Being</i></a>, in my website, <a href=\"http://www.happinessofbeing.com/\" target=\"_blank\">Happiness of Being</a>, in this <a href=\"http://happinessofbeing.blogspot.com/\">forum</a> or elsewhere, please append them as a comment to this post. Alternatively, if your comment or question relates specifically to any other post in this forum, please append it to that post.<br><br>In order to add a question or comment to this or any other post, if you are not on its own page please go to there by clicking on its title, and then click on the link 'Post a Comment', which you will find after the last comment on that page.<br><br>I will try to answer any questions that you may post in this forum as soon as I can, and since this is intended to be a forum for open discussion, <i>I also welcome</i> any answers that any other participant may like to offer.";

// const doc = new Document({
//     sections: [
//         {
//             properties: {},
//             children: [
//                 new Paragraph({
//                     children: [
//                         new TextRun(sampleText),
                      
//                     ],
//                 }),
//             ],
//         },
//     ],
// });

// // Used to export the file into a .docx file
// Packer.toBuffer(doc).then((buffer) => {
//     fs.writeFileSync("My Document.docx", buffer);
// });

(async () => {
  const fileBuffer = await HTMLtoDOCX(sampleText, null, {
    table: { row: { cantSplit: true } },
    footer: true,
    pageNumber: true,
  });

  fs.writeFile("test.docx", fileBuffer, (error) => {
    if (error) {
      console.log('Docx file creation failed');
      return;
    }
    console.log('Docx file created successfully');
  });
})();

// Done! A file called 'My Document.docx' will be in your file system.

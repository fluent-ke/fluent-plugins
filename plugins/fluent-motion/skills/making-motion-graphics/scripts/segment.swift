// macOS only (Apple Vision). Mattes for text-behind-subject and die-cut stickers.
// swift segment.swift person <shots/NAME> <masks/NAME>  → per-frame alpha mattes of the people in each frame (PNG, same names)
// swift segment.swift cutout <image> <out.png>          → the foreground subject cut out on transparency (products, logos on photos)
import Vision
import CoreImage
import AppKit
let a=CommandLine.arguments, ctx=CIContext()
func save(_ img: CIImage,_ path: String,_ rect: CGRect){
  let rep=NSBitmapImageRep(cgImage: ctx.createCGImage(img, from: rect)!)
  try! rep.representation(using: .png, properties: [:])!.write(to: URL(fileURLWithPath: path))
}
if a[1]=="person" {
  let fm=FileManager.default; try? fm.createDirectory(atPath: a[3], withIntermediateDirectories: true)
  let req=VNGeneratePersonSegmentationRequest(); req.qualityLevel = .accurate
  req.outputPixelFormat = kCVPixelFormatType_OneComponent8
  for f in try! fm.contentsOfDirectory(atPath: a[2]).filter({$0.hasSuffix(".jpg")}).sorted() {
    let url=URL(fileURLWithPath: a[2]+"/"+f), src=CIImage(contentsOf: url)!
    try! VNImageRequestHandler(url: url).perform([req])
    var m=CIImage(cvPixelBuffer: req.results!.first!.pixelBuffer)
    m=m.transformed(by: CGAffineTransform(scaleX: src.extent.width/m.extent.width, y: src.extent.height/m.extent.height))
    m=m.applyingGaussianBlur(sigma: 1.2).cropped(to: src.extent).applyingFilter("CIMaskToAlpha")
    save(m, a[3]+"/"+f.replacingOccurrences(of: ".jpg", with: ".png"), src.extent)
  }
} else {
  let url=URL(fileURLWithPath: a[2]), h=VNImageRequestHandler(url: url)
  let req=VNGenerateForegroundInstanceMaskRequest(); try! h.perform([req])
  let r=req.results!.first!
  print("instances:", r.allInstances.count)
  let pb=try! r.generateMaskedImage(ofInstances: r.allInstances, from: h, croppedToInstancesExtent: false)
  let img=CIImage(cvPixelBuffer: pb); save(img, a[3], img.extent)
}
